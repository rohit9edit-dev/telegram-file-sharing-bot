"""Migration 003: Create file table"""

def up(db):
    """Apply migration"""
    collection = db.files
    
    # Create indexes
    collection.create_index('file_id', unique=True)
    collection.create_index('user_id')
    collection.create_index('created_at')
    collection.create_index('is_deleted')
    collection.create_index('file_type')
    
    print("✅ Migration 003: File table created")

def down(db):
    """Rollback migration"""
    db.files.drop()
    print("↩️ Migration 003: File table dropped")