# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: https://www.hack4career.com
#
# Identifies what information the phishing site steals.

import os
import csv
from collections import defaultdict, Counter
from paddleocr import PaddleOCR
import matplotlib.pyplot as plt
import pandas as pd
import logging

# ⛔ Suppress DEBUG logs from ppocr
logging.getLogger("ppocr").setLevel(logging.ERROR)

# Define root folder of screenshots
ROOT_DIR = "/brand_matches"

# Define keyword categories
KEYWORDS = {
    "Credentials": ["şifre", "password", "parola", "giriş", "login", "username", "kullanıcı adı", "user name", "sifre"],
    "Identity": ["t.c. kimlik", "tc kimlik", "t.c kimlik", "soyad", "doğum tarihi", "anne kızlık", "isim", "tckn"],
    "Bank": ["kart numarası", "cvv", "iban", "hesap", "banka", "son kullanma", "kredi kartı", "kredi karti"],
    "Contact": ["cep telefonu", "e-mail", "email", "adres", "eposta", "e-posta"],
}

CSV_OUTPUT = "phishing_log.csv"

ocr = PaddleOCR(use_angle_cls=True, lang='tr')
log_rows = []

for root, _, files in os.walk(ROOT_DIR):
    for file in files:
        if file.lower().endswith(".png"):
            image_path = os.path.join(root, file)
            result = ocr.ocr(image_path, cls=True)
            detected_words = [box[1][0].lower() for line in result for box in line]

            matched = set()
            for word in detected_words:
                for category, terms in KEYWORDS.items():
                    for term in terms:
                        if term in word:
                            matched.add((category, term.lower()))

            if matched:
                print(f"\n🖼️ {os.path.relpath(image_path, ROOT_DIR)}")
                for category, keyword in matched:
                    print(f"  📌 Category: {category} | 🔑 Keyword: {keyword}")
                    log_rows.append({
                        "image": os.path.relpath(image_path, ROOT_DIR),
                        "category": category,
                        "keyword": keyword,
                    })

# Write CSV log
with open(CSV_OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["image", "category", "keyword"])
    writer.writeheader()
    for row in log_rows:
        writer.writerow(row)

print(f"\n✅ Log saved to: {CSV_OUTPUT}")

# Create pie chart
df = pd.read_csv(CSV_OUTPUT)
category_counts = df["category"].value_counts()

plt.figure(figsize=(8, 6))
plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140)
plt.title("Phishing Form Field Categories")
plt.axis('equal')
plt.tight_layout()
plt.savefig("phishing_pie_chart.png")
plt.show()
