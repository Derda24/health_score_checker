import pandas as pd
from supabase import create_client, Client
import logging
# → Supabase bilgilerinizi buraya girin:
SUPABASE_URL = "https://uhhpxxllxligtguuzogl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVoaHB4eGxseGxpZ3RndXV6b2dsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ3MjYyMTYsImV4cCI6MjA2MDMwMjIxNn0.79wVYfRcUCi5SmjJWO0h12xqE8Cr3HUxObhMc2ndJ_w"

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Load the Excel file
try:
    df = pd.read_excel("product_demi_topical.csv")
    logger.info("Excel file loaded successfully.")
except Exception as e:
    logger.error(f"Error loading Excel file: {e}")
    exit()

# Preview to confirm column names
logger.info(f"Loaded columns: {df.columns.tolist()}")

# Clean and rename columns to standardize (optional but recommended)
df.columns = [col.strip().lower() for col in df.columns]  # Standardize column names

# Check if required columns exist
required_columns = ['name', 'price', 'category', 'store_id', 'quantity']
missing = [col for col in required_columns if col not in df.columns]

if missing:
    logger.error(f"⚠️ Missing columns in Excel: {missing}")
    exit()

# Data validation function
def validate_row(row):
    # Ensure price and quantity are valid
    try:
        price = float(row['price']) if pd.notna(row['price']) else None
    except ValueError:
        price = None
        logger.warning(f"Invalid price value for product: {row['name']}")
    
    try:
        quantity = int(row['quantity']) if pd.notna(row['quantity']) else None
    except ValueError:
        quantity = None
        logger.warning(f"Invalid quantity value for product: {row['name']}")
    
    # Check for missing category and store_id
    category = row['category'].strip() if pd.notna(row['category']) else None
    store_id = row['store_id'].strip() if pd.notna(row['store_id']) else None

    # Log missing critical fields
    if not category:
        logger.warning(f"Missing category for product: {row['name']}")
    
    if not store_id:
        logger.warning(f"Missing store_id for product: {row['name']}")

    # Return the validated data
    data = {
        "name": row['name'].strip(),
        "price": price,
        "category": category,
        "store_id": store_id,
        "quantity": quantity,
    }
    return data

# Prepare data for bulk insert
data_to_insert = []
for _, row in df.iterrows():
    data = validate_row(row)
    
    # Check if required fields are not empty
    if data["name"] and data["price"] is not None and data["quantity"] is not None:
        # Ensure category and store_id are present
        if data["category"] is not None and data["store_id"] is not None:
            data_to_insert.append(data)
        else:
            logger.warning(f"Skipping row due to missing category/store_id: {row['name']}")
    else:
        logger.warning(f"Skipping row due to missing critical data (name/price/quantity): {row['name']}")

# Upload data in bulk (if any valid data exists)
if data_to_insert:
    try:
        supabase.table("products").insert(data_to_insert).execute()
        logger.info(f"✅ Successfully uploaded {len(data_to_insert)} rows.")
    except Exception as e:
        logger.error(f"Error during upload: {e}")
else:
    logger.warning("No valid data to upload.")
