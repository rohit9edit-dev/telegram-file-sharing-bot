#!/usr/bin/env python3
"""Database migration script"""
import sys
sys.path.insert(0, '/app/telegram-bot')

from database.connection import DatabaseConnection
from config import config
import importlib
import os

def run_migrations():
    """Run all pending migrations"""
    print("🛠️ Running database migrations...\n")
    
    db_conn = DatabaseConnection()
    db = db_conn.connect_sync()
    
    if not db:
        print("❌ Failed to connect to database")
        return
    
    # Get migration files
    migrations_dir = '/app/telegram-bot/database/migrations'
    migration_files = sorted([
        f for f in os.listdir(migrations_dir) 
        if f.endswith('.py') and f[0].isdigit()
    ])
    
    for migration_file in migration_files:
        migration_name = migration_file[:-3]  # Remove .py
        print(f"▶️ Running migration: {migration_name}")
        
        try:
            # Import migration module
            module = importlib.import_module(
                f'database.migrations.{migration_name}'
            )
            
            # Run up() function
            if hasattr(module, 'up'):
                module.up(db)
            else:
                print(f"⚠️  No up() function in {migration_name}")
        
        except Exception as e:
            print(f"❌ Error running {migration_name}: {e}")
    
    print("\n✅ Migrations completed!")
    db_conn.sync_client.close()

def rollback_migration(migration_name: str):
    """Rollback a specific migration"""
    print(f"↩️ Rolling back migration: {migration_name}\n")
    
    db_conn = DatabaseConnection()
    db = db_conn.connect_sync()
    
    if not db:
        print("❌ Failed to connect to database")
        return
    
    try:
        module = importlib.import_module(
            f'database.migrations.{migration_name}'
        )
        
        if hasattr(module, 'down'):
            module.down(db)
        else:
            print(f"⚠️  No down() function in {migration_name}")
    
    except Exception as e:
        print(f"❌ Error rolling back {migration_name}: {e}")
    
    db_conn.sync_client.close()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'rollback':
        if len(sys.argv) > 2:
            rollback_migration(sys.argv[2])
        else:
            print("❌ Usage: python migrate.py rollback <migration_name>")
    else:
        run_migrations()