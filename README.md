# HRMS - Human Resource Management System

A production-ready Django application for managing employees and tracking attendance with enterprise-level database reliability.

## Features

### Employee Management
- Add and manage employee records
- Edit employee information
- View comprehensive employee lists
- Smart employee ID allocation system
- Department-based organization

### Attendance Tracking
- Daily attendance marking
- Attendance history and records
- Weekly attendance reports
- Attendance statistics and analytics

## Architecture

### Database System
- **Primary**: PostgreSQL (production)
- **Backup**: SQLite (automatic failover)
- **Failover**: Automatic and transparent
- **Recovery**: Self-healing when primary returns

### Technology Stack
- **Framework**: Django 5.2.7
- **Server**: Gunicorn
- **Static Files**: WhiteNoise
- **Database**: PostgreSQL + SQLite dual-database
- **Deployment**: Docker on Render

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

Access at: http://localhost:8000

### Production Deployment

See [README_DEPLOYMENT.md](README_DEPLOYMENT.md) for complete deployment guide.

**Quick Deploy:**
1. Set environment variables in Render Dashboard
2. Push to GitHub
3. Render auto-deploys with automatic migrations

## Project Structure

```
hrms/
├── attendance/          # Attendance tracking application
├── employees/           # Employee management application
├── hrms/               # Core project settings
│   ├── settings.py     # Configuration
│   ├── db_router.py    # Database routing & failover
│   └── middleware.py   # Health monitoring
├── templates/          # HTML templates
├── Dockerfile          # Docker configuration
├── render.yaml         # Render deployment config
├── requirements.txt    # Python dependencies
└── migrate_and_sync.py # Automated migration script
```

## Database Reliability

The application uses a sophisticated dual-database architecture:

- **Normal Operation**: All data stored in PostgreSQL
- **Failover**: Automatic switch to SQLite if PostgreSQL unavailable
- **Recovery**: Automatic return to PostgreSQL when available
- **Zero Downtime**: Transparent to users

## Security

- Environment-based configuration
- No hardcoded credentials
- CSRF protection enabled
- HTTPS enforced in production
- Secure database connections

## Requirements

- Python 3.11+
- Django 5.2.7
- PostgreSQL (production)
- See requirements.txt for complete list

## Documentation

- [Deployment Guide](README_DEPLOYMENT.md) - Complete deployment instructions
- [Original Deployment Notes](DEPLOYMENT.md) - Initial deployment reference

## URL Routes

| URL | Description |
|-----|-------------|
| `/` | Employee list (root) |
| `/employees/` | Employee list |
| `/employees/add/` | Add new employee |
| `/employees/edit/<id>/` | Edit employee |
| `/employees/delete/<id>/` | Delete employee |
| `/attendance/mark/` | Mark attendance |
| `/attendance/list/` | View all attendance records |
| `/attendance/weekly/` | Weekly attendance reports |

## License

MIT
