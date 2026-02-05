# Database Configuration Guide

## Overview

This HRMS application uses a **dual-database system** with automatic failover:

- **PostgreSQL** - Primary database (production)
- **SQLite** - Backup database (fallback when PostgreSQL is unavailable)

## How It Works

### Local Development
- Uses SQLite by default (`db.sqlite3`)
- No PostgreSQL connection required
- Simple setup for development

### Production (Render)
- Uses PostgreSQL as primary database
- SQLite as automatic backup/fallback
- Seamless failover when PostgreSQL is unavailable
- Automatic migration on deployment

## Database Configuration

### Environment Variables

Set the `DATABASE_URL` environment variable to enable PostgreSQL:

```bash
DATABASE_URL=postgresql://hrms_user:ZkDSPHJRqT5cBQksQcSbpMGRscZn28ZE@dpg-d6290ongi27c73d20fc0-a/hrms_7v3v
```

**Without `DATABASE_URL`**: Application uses SQLite only (local development)
**With `DATABASE_URL`**: Application uses PostgreSQL with SQLite fallback

### Database Router

The `FallbackDatabaseRouter` (`hrms/db_router.py`) automatically:
1. Attempts to connect to PostgreSQL
2. Falls back to SQLite if PostgreSQL is unavailable
3. Periodically checks if PostgreSQL has recovered
4. Switches back to PostgreSQL when available

### Database Health Monitoring

The `DatabaseHealthMiddleware` (`hrms/middleware.py`):
- Monitors database connectivity on each request
- Logs database status changes
- Ensures smooth failover between databases

## Migration Strategy

### Automatic Migrations (Production)

The `migrate_and_sync.py` script runs automatically on deployment:

```bash
python migrate_and_sync.py
```

This script:
1. Checks PostgreSQL connectivity
2. Runs migrations on PostgreSQL (if available)
3. Runs migrations on SQLite backup
4. Ensures both databases are in sync

### Manual Migrations (Development)

For local development with SQLite:

```bash
python manage.py makemigrations
python manage.py migrate
```

For testing with PostgreSQL locally:

```bash
# Set DATABASE_URL environment variable
export DATABASE_URL=postgresql://...

# Run migrations on both databases
python migrate_and_sync.py
```

## Deployment on Render

### Configuration

The `render.yaml` file is configured for automatic deployment:

```yaml
services:
  - type: web
    name: hrms-lite
    env: python
    buildCommand: |
      pip install -r requirements.txt
      python manage.py collectstatic --noinput
    startCommand: |
      python migrate_and_sync.py && gunicorn hrms.wsgi:application
    envVars:
      - key: DATABASE_URL
        value: postgresql://...
```

### Deployment Steps

1. **Push to Repository**
   ```bash
   git add .
   git commit -m "Update database configuration"
   git push
   ```

2. **Render Auto-Deploy**
   - Render detects the push
   - Runs build command (installs dependencies, collects static files)
   - Runs start command (migrates databases, starts gunicorn)

3. **Verify Deployment**
   - Check Render logs for migration success
   - Test application functionality
   - Verify data persistence

## Database Failover Behavior

### Scenario 1: PostgreSQL Available
- All read/write operations use PostgreSQL
- SQLite backup remains synchronized
- Optimal performance

### Scenario 2: PostgreSQL Unavailable
- System automatically detects failure
- Switches to SQLite backup
- Application continues running
- Logs warning message

### Scenario 3: PostgreSQL Recovery
- System periodically checks PostgreSQL
- Automatically switches back when available
- Logs recovery message
- Resumes normal operation

## Monitoring and Logs

### Check Database Status

View logs to see which database is active:

```
INFO: PostgreSQL is available - using default database
```

or

```
WARNING: PostgreSQL unavailable - falling back to SQLite
```

### Database Health Check

The middleware logs status changes:

```
INFO: PostgreSQL connection restored - switching back from SQLite
```

or

```
WARNING: PostgreSQL connection lost - using SQLite backup
```

## Troubleshooting

### Issue: Migrations Not Running

**Solution**: Check that `migrate_and_sync.py` is being executed in the start command.

### Issue: Data Not Persisting

**Solution**: Verify DATABASE_URL is set correctly in environment variables.

### Issue: Connection Errors

**Solution**: 
1. Check PostgreSQL credentials
2. Verify network connectivity
3. Check Render database status
4. Review application logs

### Issue: SQLite Fallback Not Working

**Solution**:
1. Ensure `DATABASE_ROUTERS` is configured in settings.py
2. Check that backup database is defined
3. Verify middleware is in MIDDLEWARE list

## Best Practices

1. **Always test locally** before deploying
2. **Monitor logs** after deployment
3. **Keep SQLite backup** synchronized
4. **Use environment variables** for sensitive data
5. **Run migrations** through the automated script

## Security Notes

- Never commit database credentials to version control
- Use environment variables for DATABASE_URL
- Rotate credentials periodically
- Use SSL for PostgreSQL in production (set `ssl_require=True`)

## Support

For issues or questions:
1. Check Render deployment logs
2. Review Django application logs
3. Verify database connectivity
4. Test failover mechanism locally
