# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: https://www.hack4career.com
#
# Domain Typosquatting Analyzer
# Analyzes CSV files containing domain paths to detect brand names and typosquatting attempts.

import pandas as pd
import os
import re
from collections import defaultdict
from rapidfuzz import fuzz
import matplotlib.pyplot as plt

# Load phishing log
df = pd.read_csv("extracted_domains.csv")

# Extract domain
def extract_domain(path):
    return os.path.splitext(os.path.basename(path))[0]

# Extract brand
def extract_brand(path):
    parts = path.split("/")
    return parts[1] if len(parts) >= 2 else "Unknown"

df["domain"] = df["domain"].apply(extract_domain)
df["brand"] = df["brand"].apply(extract_brand)

# Fuzzy matching threshold
FUZZY_THRESHOLD = 80

# Store results
exact_matches = []
typosquats = []

for _, row in df.iterrows():
    domain = row["domain"].lower()
    brand = row["brand"].lower()
    domain_core = re.sub(r"[^a-z0-9]", "", domain)

    # Exact match
    if brand in domain:
        exact_matches.append((brand, domain))
    else:
        # Fuzzy match domain vs brand
        score = fuzz.partial_ratio(domain_core, brand)
        if score >= FUZZY_THRESHOLD:
            typosquats.append((brand, domain))

# Stats
total_domains = df["domain"].nunique()
typo_count = len(set([d for _, d in typosquats]))
exact_count = len(set([d for _, d in exact_matches]))
typo_ratio = typo_count / total_domains * 100 if total_domains else 0

# Display
print(f"🔍 Total Domains: {total_domains}")
print(f"✅ Exact Matches: {exact_count}")
print(f"⚠️ Typosquats: {typo_count}")
print(f"📊 Typosquatting Ratio: {typo_ratio:.2f}%\n")

print("✅ Exact Matches:")
for brand, domain in sorted(set(exact_matches)):
    print(f"{domain} (Brand: {brand})")

print("\n⚠️ Typosquats Detected:")
for brand, domain in sorted(set(typosquats)):
    print(f"{domain} (Brand: {brand})")

# Pie chart
plt.figure(figsize=(4, 4))
plt.pie(
    [exact_count, typo_count],
    labels=["Exact Match", "Typosquat"],
    autopct='%1.1f%%',
    colors=["#66bb6a", "#ef5350"],
    startangle=140
)
plt.title("Typosquatting Domain Ratio")
plt.tight_layout()
plt.show()
