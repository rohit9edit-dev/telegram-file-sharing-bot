"""Migration 001: Create user table"""

def up(db):
    """Apply migration"""
    collection = db.users
    
    # Create indexes
    collection.create_index('user_id', unique=True)
    collection.create_index('role')
    collection.create_index('created_at')
    collection.create_index('is_banned')
    
    print("✅ Migration 001: User table created")

def down(db):
    """Rollback migration"""
    db.users.drop()
    print("↩️ Migration 001: User table dropped")