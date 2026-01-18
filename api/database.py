import os
import json
import pandas as pd
from sqlalchemy import create_engine

# Database connection - adjust with your credentials
DB_URI = "postgresql://user:password@localhost:5432/medical_db"
engine = create_engine(DB_URI)

def load_raw_data(base_path):
    all_messages = []
    
    # Traverse partitioned directory structure
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Handle if data is a list of messages or a single message
                    if isinstance(data, list):
                        all_messages.extend(data)
                    else:
                        all_messages.append(data)

    if all_messages:
        df = pd.DataFrame(all_messages)
        # Ensure raw schema exists
        with engine.connect() as conn:
            conn.execute("CREATE SCHEMA IF NOT EXISTS raw;")
        
        # Load to PostgreSQL
        df.to_sql('telegram_messages', engine, schema='raw', if_exists='replace', index=False)
        print(f"Successfully loaded {len(df)} records to raw.telegram_messages")

if __name__ == "__main__":
    load_raw_data('data/raw/telegram_messages')