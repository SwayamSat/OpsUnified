import sys
import os

# Add backend to path
sys.path.append(os.getcwd())

from app.core.database import engine, Base
# Import all models to ensure they are registered with Base
from app.models import user, workspace, operations, crm, forms_inventory, system

def init_db():
    try:
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")

if __name__ == "__main__":
    init_db()
