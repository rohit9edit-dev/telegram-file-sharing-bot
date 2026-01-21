# Project Overview: Telegram File Sharing Bot

## Executive Summary

A production-ready Telegram bot built with Python (Pyrogram) that provides secure file sharing with advanced features including encryption, self-destructing links, analytics, and admin controls. Uses MongoDB for data persistence and Redis for caching.

## Project Statistics

- **Total Files**: 50+ Python files
- **Lines of Code**: ~5,000+
- **Architecture**: Clean layered architecture with separation of concerns
- **Database Models**: 7 models
- **Services**: 7 service layers
- **Handlers**: 8 command handlers
- **Plugins**: 4 extensible plugins

## Technology Stack

### Core Technologies
- **Python**: 3.8+ (Async/Await)
- **Pyrogram**: Telegram MTProto API Framework (v2.0.106)
- **MongoDB**: NoSQL Database (Motor async driver)
- **Redis**: In-memory cache (optional)

### Key Libraries
- **Pydantic**: Data validation and settings management
- **Cryptography**: File encryption and security
- **APScheduler**: Background task scheduling
- **TgCrypto**: Accelerated Telegram cryptography

## Architecture Overview

### Layer Structure

```
┌─────────────────────────────────────────┐
│           User Interface Layer          │
│         (Telegram Messages)             │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│         Handler Layer (handlers/)       │
│  - Start/Help  - Upload  - Download     │
│  - Links       - Search  - User         │
│  - Admin       - Errors                 │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│       Service Layer (services/)         │
│  - FileService    - LinkService         │
│  - UserService    - SecurityService     │
│  - AnalyticsService                     │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│     Data Access Layer (database/)       │
│  - Queries  - Models  - Migrations      │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│        Storage Layer (storage/)         │
│  - Channel Manager  - Cache Manager     │
└─────────────────────────────────────────┘
```

## Directory Structure Explained

### Core Components (`core/`)
- **client.py**: Pyrogram bot client wrapper
- **dispatcher.py**: Handler registration and routing
- **middleware.py**: Authentication, rate limiting, activity tracking
- **scheduler.py**: Background tasks (cleanup, analytics)

### Handlers (`handlers/`)
Command processors for user interactions:
- **start.py**: Welcome message, download link handler
- **upload.py**: File upload processing
- **download.py**: File download by ID
- **links.py**: Link management (list, revoke)
- **search.py**: File search functionality
- **user.py**: User stats and file listing
- **admin.py**: Admin commands (users, ban, broadcast)
- **errors.py**: Global error handling

### Services (`services/`)
Business logic layer:
- **file_service.py**: File CRUD operations, storage stats
- **link_service.py**: Link generation, validation, access control
- **user_service.py**: User management, authentication
- **security_service.py**: Encryption, password hashing
- **analytics_service.py**: Statistics calculation, caching
- **subscription_service.py**: (Future) Tier management
- **payment_service.py**: (Future) Payment processing

### Database (`database/`)

#### Models (`models/`)
Pydantic models for data validation:
- **user.py**: User accounts, roles, statistics
- **file.py**: File metadata, encryption status
- **link.py**: Download links, access control
- **access_log.py**: Download tracking
- **audit.py**: Action audit trail
- **subscription.py**: (Future) User subscriptions
- **referral.py**: (Future) Referral program

#### Queries (`queries/`)
Database operations:
- **user_queries.py**: User CRUD, statistics
- **file_queries.py**: File operations, search
- **link_queries.py**: Link management, cleanup
- **audit_queries.py**: Audit log retrieval

#### Migrations (`migrations/`)
Database schema evolution:
- **001_create_user_table.py**
- **002_add_email_to_user.py**
- **003_create_file_table.py**

### Storage (`storage/`)
- **channel_manager.py**: Telegram channel operations (upload, download, forward)
- **mirror_manager.py**: (Future) File redundancy across channels
- **cache_manager.py**: Redis caching wrapper

### Utilities (`utils/`)
- **hash.py**: Hashing, token generation
- **encryption.py**: File encryption/decryption
- **validators.py**: Input validation, sanitization
- **formatter.py**: Display formatting (file size, time, stats)
- **constants.py**: Application constants, messages

### Cache (`cache/`)
- **redis_client.py**: Redis connection and operations
- **keys.py**: Cache key patterns

### Plugins (`plugins/`)
Optional feature modules:
- **vault.py**: Encrypted file vault
- **self_destruct.py**: Time-limited files
- **watermark.py**: Media watermarking
- **experimental.py**: Batch operations, QR codes

### Scripts (`scripts/`)
Maintenance utilities:
- **migrate.py**: Run database migrations
- **cleanup.py**: Remove expired data
- **backup.py**: Database backup/restore
- **verify_setup.py**: Setup verification

## Key Features Implementation

### 1. File Upload Flow
```
User sends file → Handler validates → Forward to channel
→ Create database record → Generate download link
→ Return link to user
```

### 2. Download Link Flow
```
User clicks link → Validate link status → Check expiry/access limits
→ Retrieve file from channel → Send to user
→ Update access count → Log download
```

### 3. Self-Destruct Feature
```
Link created with timer → First access triggers countdown
→ Background task scheduled → After timeout, mark link as expired
→ Future access denied
```

### 4. Analytics System
```
Actions logged in real-time → Periodic aggregation
→ Cache in Redis → Serve from cache
→ Background refresh
```

## Database Schema

### Collections

#### users
```javascript
{
  user_id: Number (unique),
  username: String,
  first_name: String,
  role: String,  // user, admin, banned
  tier: String,  // free, basic, pro
  total_files: Number,
  total_size: Number,
  created_at: DateTime
}
```

#### files
```javascript
{
  file_id: String (unique),
  user_id: Number,
  telegram_file_id: String,
  telegram_message_id: Number,
  file_name: String,
  file_size: Number,
  file_type: String,
  is_encrypted: Boolean,
  is_deleted: Boolean,
  download_count: Number,
  created_at: DateTime
}
```

#### links
```javascript
{
  link_id: String (unique),
  file_id: String,
  user_id: Number,
  status: String,  // active, expired, revoked
  access_count: Number,
  max_access: Number,
  self_destruct: Boolean,
  expires_at: DateTime,
  created_at: DateTime
}
```

## Security Features

### 1. Access Control
- Admin-only commands via decorator
- User ban system
- Link expiry and revocation
- Max access limits per link

### 2. Data Protection
- File encryption (AES-256 via Fernet)
- Password hashing (SHA-256)
- Secure token generation
- Input sanitization

### 3. Audit Trail
- All actions logged with user ID
- Timestamp and details recorded
- Download access tracking
- Failed access attempts logged

## Performance Optimizations

### 1. Caching Strategy
- User data cached for 1 hour
- File metadata cached for 30 minutes
- Global stats cached for 6 hours
- Redis fallback to direct DB

### 2. Database Indexes
- Unique indexes on IDs
- Compound indexes on queries
- Date-based indexes for cleanup
- User ID indexes for lookups

### 3. Async Operations
- All I/O operations async
- Non-blocking database queries
- Parallel handler processing
- Background task scheduling

## Scalability Considerations

### Current Limits
- MongoDB: Handles millions of documents
- Redis: Fast in-memory caching
- Telegram: 2GB file size limit
- Bot: 30 messages/second to same user

### Scaling Options
1. **Horizontal Database Scaling**: MongoDB replica sets
2. **Cache Clustering**: Redis Cluster for distributed cache
3. **Channel Mirroring**: Multiple storage channels
4. **Load Balancing**: Multiple bot instances (webhook mode)

## Configuration Management

### Environment Variables
All sensitive data in `.env`:
- Telegram credentials
- Database connections
- Security keys
- Feature toggles

### Feature Flags
Enable/disable features:
- Analytics tracking
- File encryption
- Self-destruct
- Watermarking
- Payments

## Error Handling

### Levels
1. **Handler Level**: User-friendly error messages
2. **Service Level**: Logged exceptions, graceful degradation
3. **Global Level**: Catch-all error handler

### Logging
- Console output with colored logs
- Error traceback for debugging
- Audit logs in database
- (Future) File logging

## Testing Strategy

### Manual Testing
1. Send various file types
2. Test link expiry
3. Verify access limits
4. Check admin commands
5. Test error scenarios

### Verification Script
- Dependency check
- Configuration validation
- Database connectivity
- Redis connectivity

## Deployment Guide

### Development
```bash
python bot.py
```

### Production
1. Use process manager (systemd/PM2)
2. Configure logging to files
3. Set up monitoring
4. Regular database backups
5. Use strong encryption keys

## Maintenance

### Regular Tasks
- Daily: Check error logs
- Weekly: Run cleanup script
- Monthly: Database backup
- Quarterly: Review audit logs

### Automated Tasks
- Hourly: Expire old links
- Every 6h: Update analytics cache
- Daily: Clean old access logs
- Weekly: Database optimization

## Future Enhancements

### Planned Features
1. **Payment Integration**: Stripe/PayPal
2. **Subscription Tiers**: Different limits per tier
3. **Web Dashboard**: File management UI
4. **Mobile App**: Native mobile apps
5. **File Compression**: Reduce storage
6. **Batch Operations**: Upload multiple files
7. **User-to-User Sharing**: Direct file transfers
8. **QR Codes**: Generate for links

### Plugin System
Extensible architecture allows:
- Custom handlers
- Third-party integrations
- Feature modules
- External APIs

## Code Quality

### Best Practices
- Type hints throughout
- Async/await pattern
- Clean separation of concerns
- DRY principle
- Comprehensive error handling

### Code Organization
- Modular design
- No circular dependencies
- Clear naming conventions
- Documented functions
- Reusable utilities

## Performance Metrics

### Expected Performance
- Upload: < 5 seconds for 100MB
- Download link generation: < 1 second
- Link validation: < 100ms (cached)
- Search query: < 500ms
- Stats retrieval: < 200ms (cached)

### Resource Usage
- Memory: ~100-200MB base
- CPU: Minimal (event-driven)
- Storage: Files stored in Telegram
- Database: Metadata only (~1KB per file)

## API Design

### Handler Pattern
```python
@app.on_message(filters.command([\"command\"]))
async def handler(client, message):
    # Process command
    # Call services
    # Return response
```

### Service Pattern
```python
class Service:
    def __init__(self, db):
        self.queries = Queries(db)
    
    async def operation(self, params):
        # Business logic
        # Data validation
        # Database operations
        return result
```

## Monitoring & Analytics

### Built-in Analytics
- Total users
- Total files
- Storage usage
- Download counts
- Active links
- User activity

### Admin Dashboard
Available via `/stats_all`:
- Real-time statistics
- User growth
- Storage trends
- Popular files

## Troubleshooting Guide

### Common Issues
1. **Bot not responding**: Check token, network
2. **Upload fails**: Verify channel access
3. **Database errors**: Check MongoDB connection
4. **Cache issues**: Redis optional, bot continues

### Debug Mode
Enable verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Documentation

### Available Docs
- **README.md**: Comprehensive guide
- **QUICKSTART.md**: Fast setup guide
- **This file**: Technical overview
- **Code comments**: Inline documentation

## License & Credits

- **License**: MIT License
- **Framework**: Pyrogram
- **Database**: MongoDB
- **Cache**: Redis
- **Built for**: Telegram community

## Support & Contribution

### Getting Help
1. Check documentation
2. Review error messages
3. Check configuration
4. Open GitHub issue

### Contributing
1. Fork repository
2. Create feature branch
3. Write tests
4. Submit pull request

---

**Built with ❤️ using Python & Pyrogram**

Last Updated: 2025
Version: 1.0.0
Status: Production Ready ✅
