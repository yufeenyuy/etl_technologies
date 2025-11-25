import csv
import random
import string
import pandas as pd
import json
import os
from datetime import datetime, timedelta
from faker import Faker

# Set seed for reproducibility across all random generators
SEED = 42
random.seed(SEED)
Faker.seed(SEED)

# Initialize Faker with German locale
fake = Faker("de_DE")

# Sample German and Cameroonian names
german_first_names = ["Hans", "Karl", "Johann", "Greta", "Lukas", "Anna", "Friedrich", "Heinrich", "Sophie", "Clara"]
german_last_names = ["Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Wagner", "Becker", "Hoffmann", "Klein", "Wolf"]

cameroonian_first_names = ["Ngong", "Mbella", "Ekane", "Nkechi", "Tabe", "Fonyuy", "Ewane", "Neba", "Atangana", "Ngozi"]
cameroonian_last_names = ["Nfor", "Mbappe", "Ewane", "Ngongang", "Tchoumi", "Fokou", "Essomba", "Nkem", "Oben", "Abang"]

# Combine pools
first_names = german_first_names + cameroonian_first_names
last_names = german_last_names + cameroonian_last_names


# Generate 2000 customers
customers = []
for i in range(1, 2001):
    customer_id = f"iubi{i:04d}"  # ensures 8 characters (iubi0001 → iubi2000)
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    birth_date = fake.date_of_birth(minimum_age=20, maximum_age=75).strftime("%Y-%m-%d")
    street_name = fake.street_name()
    house_number = str(random.randint(1, 200))
    zip_code = fake.postcode()
    city = fake.city()
    state = fake.state()

    customers.append([
        customer_id, first_name, last_name, birth_date,
        street_name, house_number, zip_code, city, state
    ])

# Write to CSV

with open("customers.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "customer_id", "first_name", "last_name", "birth_date",
        "street_name", "house_number", "zip_code", "city", "state"
    ])
    writer.writerows(customers)

print("✅ customers.csv with 2000 rows has been generated (IDs iubi0001 - iubi2000).")



# Supplier attributes
company_types = ["Manufacturer", "Distributor", "Retailer", "Wholesaler", "Service Provider"]
company_sizes = ["Small", "Medium", "Large"]

suppliers = []

for i in range(1, 51):
    supplier_id = f"SUP{i:04d}"  # e.g., SUP0001 → SUP0500
    company_name = fake.company()
    street = fake.street_name()
    house_number = str(random.randint(1, 200))
    zip_code = fake.postcode()
    state = fake.state()
    company_type = random.choice(company_types)
    company_size = random.choice(company_sizes)

    suppliers.append([
        supplier_id, company_name, street, house_number,
        zip_code, state, company_type, company_size
    ])

# Write to CSV
with open("suppliers.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "supplier_id", "company_name", "street", "house_number",
        "zip_code", "state", "company_type", "company_size"
    ])
    writer.writerows(suppliers)

print("suppliers.csv with 50 rows has been generated.")


# Inventory generation in en_US locale
fake = Faker("en_US")

OUTPUT_FILE = "inventory.csv"
NUMBER_ROWS = 3000
NUM_SUPPLIERS = 50 

COLUMNS = [
    "supplier_product_id",
    "supplier_product_category",
    "supplier_product_subcategory",
    "supplier_product_quantity",
    "supplier_product_price",
    "supplier_id",
    "product_id",
    "product_name",
    "product_category",
    "product_subcategory",
    "quantity",
    "price"
]

# Categories and subcategories
CATEGORIES = {
    "Electronics": ["Smartphones", "Laptops", "Tablets", "Cameras", "Audio"],
    "Home & Kitchen": ["Appliances", "Cookware", "Storage", "Cleaning", "Decor"],
    "Office": ["Stationery", "Furniture", "Printers", "Paper", "Organization"],
    "Sports": ["Fitness", "Outdoor", "Team Sports", "Cycling", "Running"],
    "Beauty": ["Skincare", "Haircare", "Fragrance", "Makeup", "Body"],
    "Automotive": ["Accessories", "Tools", "Care", "Electronics", "Parts"],
    "Toys": ["Educational", "Action Figures", "Puzzles", "Board Games", "Dolls"],
    "Grocery": ["Beverages", "Snacks", "Pantry", "Frozen", "Produce"]
}

NAME_ADJECTIVES = [
    "Premium", "Compact", "Durable", "Eco", "Smart", "Advanced", "Classic", "Ultra", "Pro", "Lite",
    "Wireless", "Ergonomic", "Adjustable", "High-Speed", "Multi-Purpose"
]
NAME_NOUNS = [
    "Set", "Kit", "Bundle", "Device", "System", "Chair", "Mixer", "Camera", "Bottle", "Bag",
    "Helmet", "Shoes", "Monitor", "Keyboard", "Printer", "Speaker", "Lamp", "Blender", "Cleaner"
]

# Pre-generate 50 supplier IDs
SUPPLIER_IDS = [f"SUP{idx:04d}" for idx in range(1, NUM_SUPPLIERS + 1)]

# Helper function for generating product ids following consistent format
def rand_product_id(idx: int) -> str:
    return f"PROD{idx:05d}"

# Helper function for generating product names
def rand_product_name(category: str, subcategory: str) -> str:
    adj = random.choice(NAME_ADJECTIVES)
    noun = random.choice(NAME_NOUNS)
    model = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{adj} {subcategory} {noun} {model}"

# Helper function for randomly allocating quantities in a given range
def rand_quantity() -> int:
    return random.randint(1, 5000)

# Helper function for randomly allocating prices in a given range
def rand_price(category: str) -> float:
    ranges = {
        "Electronics": (50, 2000),
        "Home & Kitchen": (10, 800),
        "Office": (5, 1000),
        "Sports": (10, 1000),
        "Beauty": (2, 400),
        "Automotive": (10, 1500),
        "Toys": (5, 300),
        "Grocery": (1, 200),
    }
    low, high = ranges.get(category, (5, 500))
    return round(random.uniform(low, high), 2)

# Allocate varying row counts per supplier_id
def allocate_supplier_rows(total_rows, supplier_ids):
    """Allocate varying row counts per supplier_id, then shuffle."""
    allocations = {}
    remaining = total_rows

    # Shuffle supplier_ids so distribution order changes each run
    shuffled_ids = supplier_ids[:]
    random.shuffle(shuffled_ids)

    for sid in shuffled_ids:
        if random.random() < 0.2:  # 20% chance: very few (<10)
            count = random.randint(1, 9)
        elif random.random() < 0.3:  # 30% chance: very many (>100)
            count = random.randint(100, 200)
        else:  # otherwise moderate
            count = random.randint(20, 80)

        allocations[sid] = count
        remaining -= count

    # Adjust to exactly match total_rows
    while remaining > 0:
        sid = random.choice(shuffled_ids)
        allocations[sid] += 1
        remaining -= 1
    while remaining < 0:
        sid = random.choice(shuffled_ids)
        if allocations[sid] > 1:
            allocations[sid] -= 1
            remaining += 1

    return allocations

# Generate rows for inventory data
def generate_rows(n: int):
    rows = []
    cat_keys = list(CATEGORIES.keys())

    supplier_allocations = allocate_supplier_rows(n, SUPPLIER_IDS)

    idx = 1
    for supplier_id, count in supplier_allocations.items():
        for _ in range(count):
            category = random.choice(cat_keys)
            subcategory = random.choice(CATEGORIES[category])
            product_name = rand_product_name(category, subcategory)

            product_id = rand_product_id(idx)
            quantity = rand_quantity()
            price = rand_price(category)

            supplier_product_id = idx
            supplier_quantity = quantity + random.randint(1, 50)
            supplier_price = round(price - random.uniform(0.5, price * 0.3), 2)
            if supplier_price < 0:
                supplier_price = 0.0

            row = {
                "supplier_product_id": supplier_product_id,
                "supplier_product_category": category,
                "supplier_product_subcategory": subcategory,
                "supplier_product_quantity": supplier_quantity,
                "supplier_product_price": supplier_price,
                "supplier_id": supplier_id,
                "product_id": product_id,
                "product_name": product_name,
                "product_category": category,
                "product_subcategory": subcategory,
                "quantity": quantity,
                "price": price
            }
            rows.append(row)
            idx += 1
    return rows

def write_csv(filename: str, rows):
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


"""Generate sales_table.csv based on customer interactions log and inventory data.
This script ensures that sales transactions do not exceed available inventory."""

"""Target number of rows required for sales transactions. 
This is generated considering only custome purchase actions recorded in the log file."""
NUM_ROWS = 150000

"""
Of the 2000 unique customer and 3000 unique products, 1200 customers have generated 150,000 purchase actions.
"""
all_customers = [f"iubi{str(i).zfill(4)}" for i in range(1, 2001)]
active_customers = random.sample(all_customers, 1200)  # only 1200 make sales

# Define product IDs in the range PROD00001 - PROD03000
all_products = [f"PROD{str(i).zfill(5)}" for i in range(1, 3001)]

# Select all 3000 products
active_products = all_products

MIN_QTY, MAX_QTY = 1, 15
MIN_PRICE, MAX_PRICE = 5.0, 500.0

# Start date for transactions
start_date = datetime(2020, 1, 1)

# Output file
output_file = "sales_table.csv"

# Ensure `inventory.csv` exists. If missing, generate it first.
if not os.path.exists("inventory.csv"):
    print("inventory.csv not found — generating inventory now...")
    rows = generate_rows(NUMBER_ROWS)
    write_csv(OUTPUT_FILE, rows)
    print("inventory.csv generated.")


# Load inventory to get product quantities
inventory_df = pd.read_csv("inventory.csv")

# Create mapping of product_id to quantity
product_stock = dict(zip(inventory_df['product_id'], inventory_df['quantity']))
# Create mapping of product_id to the inventory price (use for sale price)
product_price = dict(zip(inventory_df['product_id'], inventory_df['price']))

# Track remaining stock for each product during transaction generation
remaining_stock = product_stock.copy()

# Load purchase records (logtime + customer_id) from the interactions log
purchase_records = []
try:
    with open("customer_interactions.log", "r", encoding="utf-8") as pf:
        for ln in pf:
            ln = ln.strip()
            if not ln:
                continue
            try:
                obj = json.loads(ln)
            except Exception:
                continue
            if obj.get('user_action') == 'purchase':
                lt = obj.get('logtime')
                cid = obj.get('customer_id') or obj.get('user_id') or obj.get('customer')
                if not lt:
                    continue
                # parse datetime robustly
                dt = None
                try:
                    dt = datetime.strptime(lt, "%Y-%m-%d %H:%M:%S")
                except Exception:
                    try:
                        dt = datetime.fromisoformat(lt)
                    except Exception:
                        # last resort: skip unparsable
                        continue
                purchase_records.append({'logtime': dt, 'customer_id': cid})
except FileNotFoundError:
    purchase_records = []

# Prepare exactly NUM_ROWS transaction records (time + customer_id)
transaction_records = []
if len(purchase_records) >= NUM_ROWS:
    # sample records so we get exactly NUM_ROWS purchase-based transactions
    transaction_records = random.sample(purchase_records, NUM_ROWS)
else:
    # use all purchase records first
    transaction_records = purchase_records[:]  # shallow copy

    # determine time window for synthetic fill
    if len(purchase_records) > 0:
        min_dt = min(r['logtime'] for r in purchase_records)
        max_dt = max(r['logtime'] for r in purchase_records)
    else:
        min_dt = start_date
        max_dt = start_date + timedelta(days=365 * 5)

    remaining = NUM_ROWS - len(transaction_records)
    delta_seconds = int((max_dt - min_dt).total_seconds()) if (max_dt > min_dt) else 0
    for _ in range(remaining):
        if delta_seconds > 0:
            rand_seconds = random.randint(0, delta_seconds)
            dt = min_dt + timedelta(seconds=rand_seconds)
        else:
            dt = min_dt
        cid = random.choice(all_customers)
        transaction_records.append({'logtime': dt, 'customer_id': cid})

random.shuffle(transaction_records)

# Generate data
with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow([
        "transaction_id",
        "customer_id",
        "product_id",
        "transaction_time",
        "order_quantity",
        "price",
        "sale_amount"
    ])

    transactions_written = 0
    products_sold = set()

    # Fraction of products that should be eligible for sales (changeable)
    SOLD_FRACTION = 0.8  # e.g., 0.8 means 80% of products can be sold
    num_eligible = max(1, int(len(active_products) * SOLD_FRACTION))
    eligible_products = random.sample(active_products, num_eligible)

    # Generate enough transaction IDs
    transaction_numbers = list(range(10**7, 10**7 + NUM_ROWS + 20000))
    random.shuffle(transaction_numbers)

    # Create a product list (repeated) from eligible products to randomize selection
    products_list = eligible_products * 5
    random.shuffle(products_list)

    # Top-up configuration: DISABLED for guaranteed consistency
    # All transactions must fit within initial inventory (no mid-run stock additions)
    ALLOW_TOP_UP = False

    for idx, num in enumerate(transaction_numbers):
        if transactions_written >= NUM_ROWS:
            break

        transaction_id = f"TX{num}"
        # Prefer customer_id from prepared transaction_records (which came from purchase logs).
        try:
            rec = transaction_records[transactions_written]
            customer_id = rec.get('customer_id') if rec.get('customer_id') else random.choice(active_customers)
        except Exception:
            customer_id = random.choice(active_customers)

        # Pick a product from eligible products (randomized)
        product_id = products_list[idx % len(products_list)]

        # Use the pre-prepared transaction_records list for time (and customer_id when available).
        # We only consume a record when a transaction is successfully written,
        # so use `transactions_written` index to pick the next record.
        try:
            rec_time = transaction_records[transactions_written]['logtime']
            transaction_time = rec_time
        except Exception:
            transaction_time = start_date + timedelta(
                days=random.randint(0, 365*3),
                seconds=random.randint(0, 86400)
            )

        max_available = remaining_stock.get(product_id, 0)

        # No top-ups: if stock unavailable, skip transaction
        # (with 1-3000 range, eligible products should have enough capacity)

        if max_available > 0:
            order_quantity = random.randint(1, min(MAX_QTY, max_available))
            remaining_stock[product_id] -= order_quantity

            # Use inventory price for the product when available, otherwise fallback
            price = product_price.get(product_id)
            if price is None:
                price = round(random.uniform(MIN_PRICE, MAX_PRICE), 2)
            sale_amount = round(order_quantity * price, 2)

            writer.writerow([
                transaction_id,
                customer_id,
                product_id,
                transaction_time.strftime("%Y-%m-%d %H:%M:%S"),
                order_quantity,
                price,
                sale_amount
            ])

            transactions_written += 1
            products_sold.add(product_id)

print(f"Generated {transactions_written:,} sales transactions in {output_file}")
print(f"   - Total products with sales: {len(products_sold)} / {len(active_products)}")
print(f"   - Products with NO sales: {len(active_products) - len(products_sold)}")
print(f"   - No top-ups applied (all transactions fit within initial inventory)")

# RECONCILIATION: Ensure inventory.csv matches total orders in sales_table.csv
print("\n Running reconciliation to ensure inventory consistency...")
try:
    sales_df = pd.read_csv(output_file)
    inventory_df_check = pd.read_csv(OUTPUT_FILE)  # Reload fresh from disk
    
    # Calculate total ordered per product
    summary = sales_df.groupby('product_id')['order_quantity'].sum().reset_index()
    summary.columns = ['product_id', 'total_ordered']
    
    # Merge with inventory
    merged = inventory_df_check[['product_id', 'quantity']].merge(summary, on='product_id', how='left')
    merged['total_ordered'] = merged['total_ordered'].fillna(0).astype(int)
    
    # Find oversold products
    oversold = merged[merged['total_ordered'] > merged['quantity']].copy()
    
    if len(oversold) > 0:
        print(f"Found {len(oversold)} oversold products. Adjusting inventory...")
        
        # Update inventory quantities to match total ordered
        for idx, row in oversold.iterrows():
            product_id = row['product_id']
            new_quantity = row['total_ordered']
            inventory_df_check.loc[inventory_df_check['product_id'] == product_id, 'quantity'] = new_quantity
        
        # Write corrected inventory back to disk
        inventory_df_check.to_csv(OUTPUT_FILE, index=False)
        
        total_adjusted = oversold['total_ordered'].sum() - oversold['quantity'].sum()
        print(f"Inventory reconciled: {len(oversold)} products adjusted (+{total_adjusted:,} units)")
    else:
        print(f"No oversold products found. Inventory is consistent!")
        
except Exception as e:
    print(f"Reconciliation warning: {e}")

# Inventory generation in en_US locale
def main():
    rows = generate_rows(NUMBER_ROWS)
    write_csv(OUTPUT_FILE, rows)
    print(f"Generated {NUMBER_ROWS} rows with {NUM_SUPPLIERS} unique shuffled supplier_ids to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

