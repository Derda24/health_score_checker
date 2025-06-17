import streamlit as st
from supabase import create_client, Client

# Supabase bağlantısı
url = "https://uhhpxxllxligtguuzogl.supabase.co"  # Supabase URL'niz
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVoaHB4eGxseGxpZ3RndXV6b2dsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ3MjYyMTYsImV4cCI6MjA2MDMwMjIxNn0.79wVYfRcUCi5SmjJWO0h12xqE8Cr3HUxObhMc2ndJ_w"
  # Supabase API Key'niz
supabase: Client = create_client(url, key)

# Streamlit başlığı
st.set_page_config(page_title="Health Score Checker", page_icon="🍏", layout="centered")

st.markdown("""
    <h2 style='text-align: center;'>🍎 Health Score Checker 🍎</h2>
    <p style='text-align: center;'>Check the health scores of market products!</p>
    <hr>
""", unsafe_allow_html=True)

# Ürün adı giriş
product_name = st.text_input("Enter Product Name", placeholder="e.g., Nutella, Oats, Cheese...")

if product_name:
    with st.spinner("Searching for product..."):
        # Supabase'den ürün bilgilerini çek
        result = supabase.table('products').select('*').ilike('name', f'%{product_name}%').execute()

    if result.data:  # result.data'ya erişim sağlıyoruz
        st.success("Product found!")

        # Eğer birden fazla sonuç varsa, ilkini alıyoruz
        product = result.data[0]  # İlk sonucu alıyoruz

        # Verileri düzgün şekilde görüntüle
        st.markdown(f"### 🛒 {product['name']}")
        st.markdown(f"**Category:** {product.get('category', 'Unknown')}")
        st.markdown(f"**Price:** {product.get('price', 'Not specified')}₺")
        st.markdown(f"**Store ID:** {product.get('store_id', 'N/A')}")

        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            st.metric("🏅 Health Score", product.get("health_score", "Not available"))

        with col2:
            st.metric("🔠 Grade Score", product.get("grade_score", "Not available"))

        st.markdown("---")
        st.markdown("📊 **Nutrition Facts:**")
        nutrition_facts = product.get("nutrition_facts")
        if nutrition_facts:
            for k, v in nutrition_facts.items():
                st.write(f"- {k}: {v}")
        else:
            st.write("No nutrition facts available.")
    else:
        st.error("Product not found. Please make sure the name is correct.")
else:
    st.info("No product name entered. Results will not be shown.")