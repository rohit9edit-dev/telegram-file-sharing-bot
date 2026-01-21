"""Migration 002: Add email field to user (example)"""

def up(db):
    """Apply migration"""
    # Add email field to existing users
    db.users.update_many(
        {'email': {'$exists': False}},
        {'$set': {'email': None}}
    )
    
    print("✅ Migration 002: Added email field to users")

def down(db):
    """Rollback migration"""
    # Remove email field
    db.users.update_many(
        {},
        {'$unset': {'email': ''}}
    )
    
    print("↩️ Migration 002: Removed email field from users")