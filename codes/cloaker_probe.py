#!/usr/bin/env python3
"""
Author: Mert SARICA
E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
URL: https://www.hack4career.com

Probe cloaked phishing URLs by cycling UA/Referer and geo-proxies.

Detection: keyword-only. Supports Turkish keywords to reduce FPs.
Choose keywords with --keywords tr|en|both (default: tr).

Examples
  python cloaker_probe.py --url https://roogba.info/ --proxy-json proxy.json --http2
  python cloaker_probe.py --url https://roogba.info/ --proxy-json proxy.json --only ES,US --with-direct --http2
  python cloaker_probe.py --url https://roogba.info/ --http2 --with-direct    # no proxies, just UA/Ref permutations
"""

import argparse
import asyncio
import csv
import json
import random
import re
import sys
from itertools import product
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

import httpx

# -------- httpx proxy kw compatibility (supports both old/new httpx) --------
try:
    _HTTPX_VER = tuple(int(x) for x in httpx.__version__.split(".")[:2])
    _PROXY_KW = "proxy" if _HTTPX_VER >= (0, 28) else "proxies"
except Exception:
    _PROXY_KW = "proxies"

# -------- Defaults --------

DEFAULT_UAS: List[str] = [
    # Desktop
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",

    # Mobile
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36",

    # Social/preview bots (often whitelisted)
    "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
    "Twitterbot/1.0",
    "TelegramBot (like TwitterBot)",
    "Slackbot-LinkExpanding 1.0 (+https://api.slack.com/robots)",
    "LinkedInBot/1.0 (+https://www.linkedin.com)"
]

DEFAULT_REFERERS: List[Optional[str]] = [
    None,  # no Referer
    "https://m.facebook.com/",
    "https://www.facebook.com/",
    "https://l.facebook.com/",
    "https://x.com/",
    "https://t.co/",
    "https://telegram.me/",
    "https://web.telegram.org/",
    "https://wa.me/",
    "https://www.linkedin.com/",
    "https://www.instagram.com/",
    "https://www.google.com/"
]

# -------- Keyword sets (English & Turkish) --------
PHISH_KEYWORDS_EN = [
    "login", "log in", "sign in", "verify", "verification", "security check",
    "password", "passcode", "card number", "update account",
    "otp", "one-time password", "one time password",
    "2fa", "two-factor", "two factor", "ssn"
]

PHISH_KEYWORDS_TR = [
    "giriş", "oturum aç", "oturum açın", "doğrula", "doğrulama", "güvenlik kontrolü",
    "şifre", "parola", "şifrenizi", "parolanız", "kart numarası", "kart no",
    "hesap güncelle", "hesabınızı güncelleyin", "hesap doğrulama", "kimlik doğrulama",
    "tek kullanımlık şifre", "tek kullanımlık kod", "sms şifresi", "onay kodu",
    "iki adımlı", "iki faktörlü", "2 adımlı", "2 faktörlü"
]

def build_keywords(mode: str) -> List[str]:
    mode = (mode or "tr").lower()
    if mode == "tr":
        return PHISH_KEYWORDS_TR
    if mode == "en":
        return PHISH_KEYWORDS_EN
    # both
    return list(dict.fromkeys(PHISH_KEYWORDS_TR + PHISH_KEYWORDS_EN))

# -------- Utils --------

def dedupe(seq):
    seen = set()
    out = []
    for x in seq:
        key = (x or "").lower()
        if key not in seen:
            seen.add(key)
            out.append(x)
    return out

def parse_kv_list(items: List[str]) -> Dict[str, str]:
    out = {}
    for it in items or []:
        if "=" in it:
            k, v = it.split("=", 1)
            out[k.strip()] = v.strip()
    return out

def build_proxy_url(entry: dict) -> Optional[str]:
    """
    Build a proxy URL from a proxy.json entry like:
      {
        "active": true,
        "title": "ES",
        "type": "http",
        "hostname": "pool.infatica.io",
        "port": "10011",
        "username": "...",
        "password": "...",
        ...
      }
    Returns e.g. "http://user:pass@pool.infatica.io:10011"
    Supports type: http, https, socks5
    """
    if not entry.get("active", True):
        return None
    scheme = (entry.get("type") or "http").lower()
    host = entry.get("hostname")
    port = str(entry.get("port") or "").strip()
    user = entry.get("username") or ""
    pwd  = entry.get("password") or ""
    if not host or not port:
        return None
    if scheme not in {"http", "https", "socks5"}:
        scheme = "http"
    auth = f"{user}:{pwd}@" if user else ""
    return f"{scheme}://{auth}{host}:{port}"

def load_proxies_from_json(path: str, sample_n: Optional[int] = None) -> Dict[str, str]:
    """
    Loads proxy.json and returns {label: proxy_url}.
    Label preference: entry['title'] or entry['cc'] or 'PROXY_i'.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    entries = data.get("data") or []
    built = []
    for i, e in enumerate(entries):
        url = build_proxy_url(e)
        if not url:
            continue
        label = (e.get("title") or e.get("cc") or f"PROXY_{i}").strip() or f"PROXY_{i}"
        built.append((label, url))

    if sample_n is not None and sample_n > 0 and sample_n < len(built):
        built = random.sample(built, sample_n)

    # Deduplicate labels
    result: Dict[str, str] = {}
    counts: Dict[str, int] = {}
    for label, url in built:
        if label in result:
            counts[label] = counts.get(label, 1) + 1
            label = f"{label}_{counts[label]}"
        result[label] = url
    return result

# -------- Detection (keyword-only) --------

def score_phish_keyword_only(html_text: str, keywords: List[str]) -> Tuple[bool, str]:
    """
    Minimal: PHISH if page contains any phishing keywords (EN/TR based on --keywords).
    HTTP status code is not used directly here; the caller prints it but only keywords trigger PHISH.
    """
    low = (html_text or "").lower()
    if any(k in low for k in keywords):
        return True, "phish_keywords"
    return False, "no_phish_signals"

# -------- HTTP work --------

async def fetch_once(
    url: str,
    ua: str,
    referer: Optional[str],
    proxy_url: Optional[str],
    http2: bool,
    extra_headers: Dict[str, str],
    keywords: List[str],
    timeout_s: float = 20.0,
    jitter_range: Tuple[float, float] = (0.05, 0.3),
) -> Dict[str, str]:
    headers = {
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Pragma": "no-cache",
    }
    if referer:
        headers["Referer"] = referer
    if extra_headers:
        headers.update(extra_headers)

    limits = httpx.Limits(max_connections=1, max_keepalive_connections=0)
    proxy_kwargs = ({_PROXY_KW: proxy_url} if proxy_url else {})

    await asyncio.sleep(random.uniform(*jitter_range))

    try:
        async with httpx.AsyncClient(
            http2=http2,
            timeout=timeout_s,
            limits=limits,
            follow_redirects=True,
            **proxy_kwargs,
        ) as client:
            resp = await client.get(url, headers=headers)
            final_url = str(resp.url)
            status = resp.status_code
            text = resp.text[:300000]
            clen = len(text or "")
            is_phish, reason = score_phish_keyword_only(text, keywords)
            outcome = "PHISH" if is_phish else "FAKE"
            return {
                "status": str(status),
                "final_url": final_url,
                "content_len": str(clen),
                "outcome": outcome,
                "reason": reason,
            }
    except httpx.HTTPError as e:
        return {
            "status": "ERR",
            "final_url": "",
            "content_len": "0",
            "outcome": "ERROR",
            "reason": f"http_error:{type(e).__name__}",
        }

# -------- Orchestrator --------

async def run_probe(
    url: str,
    uas: List[str],
    referers: List[Optional[str]],
    proxies: Dict[str, str],
    only_labels: Optional[List[str]],
    include_direct: bool,
    out_csv: str,
    http2: bool,
    global_concurrency: int,
    per_proxy_concurrency: int,
    extra_headers: Dict[str, str],
    keywords: List[str],
):
    # Filter proxies if --only provided
    if only_labels:
        proxies = {k: v for k, v in proxies.items() if k in set(only_labels)}
        if not proxies and not include_direct:
            print("No proxies left after --only filter.", file=sys.stderr)
            sys.exit(2)

    # Concurrency controls
    global_sem = asyncio.Semaphore(global_concurrency)
    proxy_sems: Dict[str, asyncio.Semaphore] = {label: asyncio.Semaphore(per_proxy_concurrency) for label in proxies}

    combos = []
    # Proxied combos
    for label, purl in proxies.items():
        for ua, ref in product(uas, referers):
            combos.append((label, purl, ua, ref))
    # Direct combos if requested or if no proxies given
    if include_direct or not proxies:
        for ua, ref in product(uas, referers):
            combos.append(("DIRECT", None, ua, ref))

    results_rows: List[Dict[str, str]] = []

    async def worker(label: str, proxy_url: Optional[str], ua: str, ref: Optional[str]):
        async with global_sem:
            sem = proxy_sems.get(label) or asyncio.Semaphore(1)
            async with sem:
                res = await fetch_once(
                    url=url,
                    ua=ua,
                    referer=ref,
                    proxy_url=proxy_url,
                    http2=http2,
                    extra_headers=extra_headers,
                    keywords=keywords,
                )
                row = {
                    "proxy_label": label,
                    "proxy_url": proxy_url or "",
                    "user_agent": ua,
                    "referer": ref or "",
                    **res,
                }
                results_rows.append(row)
                short_ref = "(none)" if not ref else (ref.split("/")[2] if "://" in ref else ref)
                print(f"[{row['outcome']:<5}] {label:<10} UA={'bot' if 'bot' in ua.lower() else 'ua':<3} Ref={short_ref:<12} -> {row['status']}  {row['final_url'] or '(error)'}  reason={row['reason']}")

    tasks = [asyncio.create_task(worker(label, purl, ua, ref)) for (label, purl, ua, ref) in combos]
    await asyncio.gather(*tasks)

    # Sort results: PHISH first, then by proxy label
    results_rows.sort(key=lambda r: (r["outcome"] != "PHISH", r["proxy_label"], r["reason"], r["user_agent"], r["referer"]))

    fieldnames = [
        "outcome", "reason", "status", "final_url", "content_len",
        "proxy_label", "proxy_url", "user_agent", "referer"
    ]
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in results_rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})

    print("\n=== PHISH-LIKELY COMBINATIONS ===")
    any_phish = False
    for r in results_rows:
        if r["outcome"] == "PHISH":
            any_phish = True
            print(f"- [{r['proxy_label']}] UA: {r['user_agent'][:90]}...")
            print(f"  Ref: {r['referer'] or '(none)'}")
            print(f"  -> {r['final_url']}  [{r['status']}] reason={r['reason']}")
    if not any_phish:
        print("(none detected; try other geos, vary Referer/UA, or switch --keywords to 'both').")

# -------- Main --------

def main():
    ap = argparse.ArgumentParser(description="Probe cloaked phishing URLs with UA/Referer and proxies from proxy.json (keyword-only detection).")
    ap.add_argument("--url", required=True, help="Landing URL to test (e.g., https://roogba.info/)")
    ap.add_argument("--out", default="cloaker_results.csv", help="CSV output file")
    ap.add_argument("--http2", action="store_true", help="Enable HTTP/2")
    ap.add_argument("--concurrency", type=int, default=10, help="Global concurrency across all proxies (default: 10)")
    ap.add_argument("--per-proxy-concurrency", type=int, default=2, help="Concurrency per proxy label (default: 2)")

    # Headers & wordlists
    ap.add_argument("--header", action="append", help="Extra header(s), KEY=VALUE (can repeat)")
    ap.add_argument("--ua-file", help="Append newline-separated User-Agents")
    ap.add_argument("--ref-file", help="Append newline-separated Referers")
    ap.add_argument("--keywords", choices=["tr", "en", "both"], default="tr",
                    help="Which keyword set to use for detection (default: tr)")

    # JSON proxies
    ap.add_argument("--proxy-json", help="Path to proxy.json (contains 'data' list of proxies)")
    ap.add_argument("--only", help="Comma-separated labels (title/cc from JSON) to use")
    ap.add_argument("--sample-proxies", type=int, help="Randomly sample N proxies from JSON (after filtering)")
    ap.add_argument("--with-direct", action="store_true", help="Also test without proxy (DIRECT)")

    args = ap.parse_args()

    uas = dedupe(DEFAULT_UAS)
    refs = dedupe(DEFAULT_REFERERS)

    if args.ua_file:
        try:
            with open(args.ua_file, "r", encoding="utf-8") as f:
                uas.extend([ln.strip() for ln in f if ln.strip()])
        except Exception as e:
            print(f"Failed to read --ua-file: {e}", file=sys.stderr)
    if args.ref_file:
        try:
            with open(args.ref_file, "r", encoding="utf-8") as f:
                refs.extend([ln.strip() for ln in f if ln.strip()])
        except Exception as e:
            print(f"Failed to read --ref-file: {e}", file=sys.stderr)

    uas = dedupe(uas)
    refs = dedupe(refs)

    extra_headers = parse_kv_list(args.header) if args.header else {}
    keywords = build_keywords(args.keywords)

    proxies: Dict[str, str] = {}
    if args.proxy_json:
        try:
            proxies = load_proxies_from_json(args.proxy_json, sample_n=args.sample_proxies)
        except Exception as e:
            print(f"Failed to read --proxy-json: {e}", file=sys.stderr)
            sys.exit(2)

    only_labels = [s.strip() for s in args.only.split(",")] if args.only else None

    asyncio.run(run_probe(
        url=args.url,
        uas=uas,
        referers=refs,
        proxies=proxies,
        only_labels=only_labels,
        include_direct=args.with_direct or not proxies,  # if no proxies, run DIRECT by default
        out_csv=args.out,
        http2=args.http2,
        global_concurrency=args.concurrency,
        per_proxy_concurrency=args.per_proxy_concurrency,
        extra_headers=extra_headers,
        keywords=keywords,
    ))

if __name__ == "__main__":
    main()

