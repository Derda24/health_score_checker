import pandas as pd
import requests

# Excel dosyasını yükle
df = pd.read_excel("products_lidl_topical.xlsx")

def fetch_openfoodfacts_data(product_name):
    try:
        response = requests.get(
            "https://world.openfoodfacts.org/cgi/search.pl",
            params={
                "search_terms": product_name,
                "search_simple": 1,
                "action": "process",
                "json": 1,
            },
            timeout=5
        )
        data = response.json()
        if data["count"] == 0:
            return None, None
        product = data["products"][0]
        return product.get("nutriscore_score"), product.get("nutriscore_grade")
    except Exception:
        return None, None

# Eksik skorları doldur
for idx, row in df.iterrows():
    if pd.isna(row['health_score']) or row['health_score'] == "Error":
        health, grade = fetch_openfoodfacts_data(row['name'])
        if health is not None:
            df.at[idx, 'health_score'] = health
        if grade is not None:
            df.at[idx, 'grade_score'] = grade

# Güncellenmiş Excel dosyasını kaydet
df.to_excel("products_lidl_topical_updated.xlsx", index=False)
