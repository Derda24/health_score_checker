import pandas as pd
import math
from supabase import create_client, Client

# → Supabase bilgilerinizi buraya girin:
SUPABASE_URL = "https://uhhpxxllxligtguuzogl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVoaHB4eGxseGxpZ3RndXV6b2dsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ3MjYyMTYsImV4cCI6MjA2MDMwMjIxNn0.79wVYfRcUCi5SmjJWO0h12xqE8Cr3HUxObhMc2ndJ_w"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ——— Excel'den oku ———
df = pd.read_excel("products_lidl_topical.xlsx")

def clean(v, field_name=""):
    if field_name == "name":
        if v is None:
            return "Unnamed Product"
        v_str = str(v).strip()
        return v_str if v_str else "Unnamed Product"

    if v is None or v == "" or v == "Error":
        return None
    if isinstance(v, (int, float)):
        return v if math.isfinite(v) else None
    try:
        # Virgülleri noktaya çevirerek float dönüşümüne izin verelim:
        return float(str(v).replace(",", "."))
    except:
        return None


# ——— Records listesi: ———
records = []
for idx, row in df.iterrows():
    name = clean(row["name"], field_name="name")
    if not name:
        print(f"❌ Satır {idx} boş name ile atlandı: {row.to_dict()}")
        continue  # name boşsa bu satırı atla
    records.append({
    "name":         clean(row["name"], field_name="name"),
    "price":        clean(row["price"]),
    "category":     clean(row["category"]),
    "store_id":     clean(row["store_id"]),
    "dimension":    clean(row["dimension"]),
    "health_score": clean(row.get("health_score")),
    "grade_score":  clean(row.get("grade_score")),
})


# ——— Insert edin ———
response = supabase.table("products").insert(records).execute()

# ——— Inspect edelim ———
print("┌─ raw response object ──────────────────────────────────────────")
print(response)
print("└───────────────────────────────────────────────────────────────\n")

# Pydantic BaseModel, .dict() ile tüm alanları gösterir:
try:
    print("┌─ response as dict ───────────────────────────────────────────")
    print(response.dict())
    print("└─────────────────────────────────────────────────────────────\n")
except:
    pass

# Şimdi olası alanları ele alalım:
if hasattr(response, "data"):
    print("✅ response.data (inserted):", len(response.data), "kayıt")
if hasattr(response, "status_code"):
    print("🔢 response.status_code:", response.status_code)
if hasattr(response, "count"):
    print("🔢 response.count:", response.count)
if hasattr(response, "error"):
    print("❌ response.error:", response.error)