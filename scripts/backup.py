#!/usr/bin/env python3
"""Database backup script"""
import sys
sys.path.insert(0, '/app/telegram-bot')

import asyncio
from datetime import datetime
from database.connection import DatabaseConnection
import json
import os

async def backup_collection(db, collection_name: str, output_dir: str):
    """Backup a single collection"""
    print(f"💾 Backing up {collection_name}...")
    
    collection = db[collection_name]
    cursor = collection.find({})
    
    documents = []
    async for doc in cursor:
        # Remove MongoDB _id for JSON serialization
        doc.pop('_id', None)
        # Convert datetime to ISO format
        for key, value in doc.items():
            if isinstance(value, datetime):
                doc[key] = value.isoformat()
        documents.append(doc)
    
    # Save to JSON file
    output_file = os.path.join(output_dir, f"{collection_name}.json")
    with open(output_file, 'w') as f:
        json.dump(documents, f, indent=2)
    
    print(f"✅ Backed up {len(documents)} documents to {output_file}")
    return len(documents)

async def backup_database():
    """Backup entire database"""
    print("💾 Starting database backup...\n")
    
    db_conn = DatabaseConnection()
    await db_conn.connect()
    db = db_conn.db
    
    # Create backup directory
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    backup_dir = f"/tmp/backups/backup_{timestamp}"
    os.makedirs(backup_dir, exist_ok=True)
    
    # Collections to backup
    collections = ['users', 'files', 'links', 'access_logs', 'audit_logs']
    
    total_docs = 0
    for collection in collections:
        count = await backup_collection(db, collection, backup_dir)
        total_docs += count
    
    # Create metadata file
    metadata = {
        'backup_date': timestamp,
        'total_documents': total_docs,
        'collections': collections
    }
    
    with open(os.path.join(backup_dir, 'metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n✅ Backup completed!")
    print(f"📁 Location: {backup_dir}")
    print(f"📊 Total documents: {total_docs}")
    
    await db_conn.disconnect()

async def restore_database(backup_dir: str):
    """Restore database from backup"""
    print(f"💾 Restoring database from {backup_dir}...\n")
    
    if not os.path.exists(backup_dir):
        print("❌ Backup directory not found")
        return
    
    db_conn = DatabaseConnection()
    await db_conn.connect()
    db = db_conn.db
    
    # Read metadata
    metadata_file = os.path.join(backup_dir, 'metadata.json')
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        collections = metadata['collections']
    else:
        # Find all JSON files
        collections = [
            f[:-5] for f in os.listdir(backup_dir) 
            if f.endswith('.json') and f != 'metadata.json'
        ]
    
    total_restored = 0
    for collection_name in collections:
        file_path = os.path.join(backup_dir, f"{collection_name}.json")
        if not os.path.exists(file_path):
            continue
        
        print(f"🔄 Restoring {collection_name}...")
        
        with open(file_path, 'r') as f:
            documents = json.load(f)
        
        if documents:
            collection = db[collection_name]
            await collection.insert_many(documents)
            total_restored += len(documents)
            print(f"✅ Restored {len(documents)} documents to {collection_name}")
    
    print(f"\n✅ Restore completed!")
    print(f"📊 Total documents restored: {total_restored}")
    
    await db_conn.disconnect()

async def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == 'restore':
        if len(sys.argv) > 2:
            await restore_database(sys.argv[2])
        else:
            print("❌ Usage: python backup.py restore <backup_directory>")
    else:
        await backup_database()

if __name__ == '__main__':
    asyncio.run(main())