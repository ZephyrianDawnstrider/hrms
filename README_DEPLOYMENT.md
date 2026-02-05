# HRMS Application - Deployment Guide

## Overview

This HRMS (Human Resource Management System) application uses Django with a robust dual-database architecture for high availability and data redundancy.

## Architecture

### Database System
- **Primary Database**: PostgreSQL (production)
- **Backup Database**: SQLite (automatic failover)
- **Failover**: Automatic and transparent
- **Recovery**: Automatic when primary database returns

### Technology Stack
- **Framework**: Django 5.2.7
- **Server**: Gunicorn
- **Static Files**: WhiteNoise
- **Database**: PostgreSQL + SQLite
- **Deployment**: Docker on Render

## Local Development

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

The application uses SQLite locally for simplicity. No PostgreSQL setup required for development.

### Access
- Local URL: http://127.0.0.1:8000
- Database: SQLite (db.sqlite3)

## Production Deployment on Render

### Prerequisites
1. GitHub repository with your code
2. Render account
3. PostgreSQL database on Render

### Environment Variables

Set these in Render Dashboard → Your Service → Environment:

| Variable | Value | How to Set |
|----------|-------|------------|
| `DATABASE_URL` | Auto-generated | Link from PostgreSQL database |
| `ALLOWED_HOSTS` | `your-app.onrender.com` | Manual entry |
| `CSRF_TRUSTED_ORIGINS` | `https://your-app.onrender.com` | Manual entry |
| `SECRET_KEY` | Auto-generated | Already set by Render |
| `DEBUG` | `False` | Already set |

#### Setting DATABASE_URL
1. Go to your web service → Environment tab
2. Click "Add from Database"
3. Select your PostgreSQL database
4. Render automatically creates the DATABASE_URL

### Deployment Process

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy HRMS application"
   git push origin main
   ```

2. **Automatic Deployment**
   - Render detects the push
   - Builds Docker image
   - Runs migrations automatically
   - Starts the application

3. **Verify Deployment**
   - Check logs for successful migrations
   - Visit your application URL
   - Test functionality

### Expected Deployment Logs

```
Building Docker image...
Deploying...
INFO: HRMS Database Migration Script
INFO: ✓ Database 'default' is accessible
INFO: Running migrations on 'default' database...
INFO: ✓ Migrations completed successfully
[INFO] Starting gunicorn 21.2.0
==> Your service is live 🎉
```

## Database Failover

### How It Works

The application automatically handles database failures:

1. **Normal Operation**: All requests use PostgreSQL
2. **PostgreSQL Fails**: System detects failure and switches to SQLite backup
3. **Application Continues**: Users experience no downtime
4. **PostgreSQL Recovers**: System automatically switches back

### Monitoring

Check application logs to see active database:
- `PostgreSQL is available` - Using primary database
- `PostgreSQL unavailable - falling back to SQLite` - Using backup

## Features

### Employee Management
- Add new employees
- Edit employee information
- View employee list
- Check available employee IDs

### Attendance Tracking
- Mark daily attendance
- View attendance records
- Weekly attendance reports
- Attendance statistics

## Troubleshooting

### Issue: Application won't start

**Check:**
1. Environment variables are set correctly
2. DATABASE_URL is linked from PostgreSQL
3. PostgreSQL database is running

**Solution:**
- Verify all environment variables in Render Dashboard
- Check deployment logs for specific errors

### Issue: Data not persisting

**Check:**
1. DATABASE_URL is set
2. Migrations completed successfully

**Solution:**
- Redeploy using "Manual Deploy" button in Render Dashboard
- Check logs for migration errors

### Issue: Need to re-run migrations

**Solution:**
1. Go to Render Dashboard → Your Service
2. Click "Manual Deploy" button
3. Select "Deploy latest commit"
4. Migrations run automatically

## Security

- All sensitive credentials use environment variables
- No hardcoded passwords or secrets
- Database credentials never committed to Git
- HTTPS enforced in production
- CSRF protection enabled

## File Structure

```
hrms/
├── attendance/          # Attendance tracking app
├── employees/           # Employee management app
├── hrms/               # Project settings
│   ├── settings.py     # Configuration
│   ├── db_router.py    # Database routing
│   └── middleware.py   # Health monitoring
├── templates/          # HTML templates
├── Dockerfile          # Docker configuration
├── render.yaml         # Render deployment config
├── requirements.txt    # Python dependencies
└── migrate_and_sync.py # Migration automation
```

## Maintenance

### Updating Dependencies
```bash
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
git commit -am "Update dependencies"
git push
```

### Database Backups
- PostgreSQL: Managed by Render (automatic backups)
- SQLite: Included in deployment (automatic sync)

### Monitoring
- Check Render Dashboard for service health
- Review logs regularly
- Monitor database performance

## Support

For deployment issues:
1. Check Render deployment logs
2. Verify environment variables
3. Ensure PostgreSQL database is running
4. Review application logs

---

## Technical Notes

<details>
<summary>Database Configuration Details</summary>

The application uses a custom database router (`hrms/db_router.py`) that:
- Attempts PostgreSQL connection first
- Falls back to SQLite on connection failure
- Periodically checks PostgreSQL health
- Automatically recovers when PostgreSQL is available

Configuration is environment-aware:
- **Local**: Uses SQLite only (no DATABASE_URL)
- **Production**: Uses PostgreSQL with SQLite backup (DATABASE_URL set)
</details>

<details>
<summary>Migration Strategy</summary>

Migrations run automatically via `migrate_and_sync.py`:
- Runs at container startup (not build time)
- Migrates both PostgreSQL and SQLite
- Handles connection failures gracefully
- Logs migration status

This ensures migrations have access to the DATABASE_URL environment variable.
</details>

<details>
<summary>Render Free Tier Compatibility</summary>

This application is optimized for Render's free tier:
- No shell access required
- All configuration via Dashboard
- Automatic migrations on deployment
- Manual redeploy available via Dashboard
- Log monitoring through web interface
</details>

---

**Version**: 1.0  
**Last Updated**: February 2026  
**Django Version**: 5.2.7
