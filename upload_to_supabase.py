import pandas as pd
import requests

# Supabase bilgilerin
SUPABASE_URL = "https://uhhpxxllxligtguuzogl.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVoaHB4eGxseGxpZ3RndXV6b2dsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ3MjYyMTYsImV4cCI6MjA2MDMwMjIxNn0.79wVYfRcUCi5SmjJWO0h12xqE8Cr3HUxObhMc2ndJ_w"

headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

# Excel dosyasını oku
df = pd.read_excel("products_lidl_guncel.xlsx")

# Her satırı Supabase'e yolla
for _, row in df.iterrows():
    data = {
        "name": row["name"],
        "price": row["price"],
        "category": row["category"],
        "store_id": row["store_id"],
        "health_score": row.get("health_score", None),
        "grade_score": row.get("grade_score", None),
    }
    response = requests.post(SUPABASE_URL, json=data, headers=headers)
    print(response.status_code, response.text)
