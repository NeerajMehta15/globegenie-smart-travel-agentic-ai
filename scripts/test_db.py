# test_db.py
from db.database import init_db, get_db_info

# Initialize database
print("Initializing database...")
init_db()

# Check status
print("\nDatabase info:")
info = get_db_info()
for key, value in info.items():
    print(f"  {key}: {value}")