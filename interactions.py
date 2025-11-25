import random
import json
from datetime import datetime, timedelta

# Set seed for reproducibility
SEED = 42
random.seed(SEED)

# Number of interactions
NUM_INTERACTIONS = 350000
NUM_PURCHASES = 150000  # Exactly 150,000 purchase actions

# Customer IDs
customers = [f"iubi{str(i).zfill(4)}" for i in range(1, 2001)]

# Example pages and actions
pages = ["home", "product_page", "search", "cart", "checkout", "profile", "support"]
actions = ["view", "click", "scroll", "add_to_cart", "remove_from_cart", "purchase", "search", "logout"]

# Example search queries
search_queries = [
    "laptop", "smartphone", "headphones", "gaming chair", "coffee maker",
    "books", "shoes", "jackets", "wireless mouse", "keyboard", "monitor",
    "fitness tracker", "backpack", "camera", "tablet"
]

# Start date for logs
start_date = datetime(2022, 1, 1)
purchase_start_date = datetime(2022, 5, 1)
end_date = datetime(2025, 10, 31)

# Output log file
output_file = "customer_interactions.log"

# Generate unique session IDs
session_ids = [f"SESS{str(i).zfill(7)}" for i in range(1, NUM_INTERACTIONS + 1)]

# Generate data
days_span = (end_date - start_date).days

# First pass: generate all logs and collect their times
temp_logs = []
for i in range(NUM_INTERACTIONS):
    logtime = start_date + timedelta(
        days=random.randint(0, days_span),
        seconds=random.randint(0, 86400)
    )
    temp_logs.append({
        'index': i,
        'logtime': logtime,
        'session': session_ids[i],
        'customer_id': random.choice(customers),
        'page_visit': random.choice(pages),
        'session_duration_sec': random.randint(10, 3600),
        'search_query': random.choice(search_queries) if random.random() < 0.9 else ""
    })

# Second pass: assign purchase actions to logs that occur on or after purchase_start_date
eligible_indices = [idx for idx, log in enumerate(temp_logs) if log['logtime'] >= purchase_start_date]
purchase_indices = set(random.sample(eligible_indices, min(NUM_PURCHASES, len(eligible_indices))))

# Third pass: write logs with assigned actions
with open(output_file, mode="w", encoding="utf-8") as file:
    for idx, log in enumerate(temp_logs):
        if idx in purchase_indices:
            user_action = 'purchase'
        else:
            available_actions = [a for a in actions if a != 'purchase']
            user_action = random.choice(available_actions)
        
        log_entry = {
            "logtime": log['logtime'].strftime("%Y-%m-%d %H:%M:%S"),
            "session": log['session'],
            "customer_id": log['customer_id'],
            "page_visit": log['page_visit'],
            "user_action": user_action,
            "session_duration_sec": log['session_duration_sec'],
            "search_query": log['search_query']
        }
        
        file.write(json.dumps(log_entry) + "\n")

print(f"✅ Generated {NUM_INTERACTIONS} JSON log entries in {output_file}")
