# Quick Start Guide - HRMS Deployment

## Summary of Your Current Setup

### ✅ What's Working Now:
- **Local Development**: Using SQLite database
- **Server Running**: Django development server at http://127.0.0.1:8000
- **Security**: No credentials hardcoded in code
- **Database System**: PostgreSQL with SQLite fallback implemented

### 📊 Current Database Status:
- **Active Database**: SQLite (`db.sqlite3`)
- **Reason**: No `DATABASE_URL` environment variable set
- **This is correct** for local development!

## Answer to Your Questions

### 1. Which database is being used right now?
**SQLite** - Because you're running locally without the `DATABASE_URL` environment variable set.

### 2. Is it okay to hardcode the database URL?
**NO! ❌** - I've removed the hardcoded URL from `render.yaml` for security reasons.

**Why it's dangerous:**
- Anyone with access to your Git repository can see the password
- If you push to GitHub (public or private), credentials are exposed
- Database could be compromised

**The secure way:**
- Set `DATABASE_URL` in Render's dashboard (Environment Variables)
- Render provides the internal database URL automatically
- Never commit credentials to Git

## How to Deploy to Render (Secure Method)

### Step 1: Prepare Your Code
```bash
# Make sure all changes are committed
git add .
git commit -m "Implement PostgreSQL with SQLite fallback - secure setup"
git push origin main
```

### Step 2: Set Up Database on Render

**Option A: Link Existing Database (Recommended)**
1. Go to Render Dashboard
2. Open your web service (hrms-lite)
3. Click "Environment" tab
4. Click "Add from Database"
5. Select your PostgreSQL database
6. Render automatically creates `DATABASE_URL` ✅

**Option B: Manual Setup**
1. Go to your PostgreSQL database in Render
2. Copy the **Internal Database URL**
3. Go to your web service
4. Environment → Add Environment Variable
5. Key: `DATABASE_URL`
6. Value: Paste the Internal URL
7. Save

### Step 3: Set Other Environment Variables

In Render → Your Web Service → Environment, add:

```
ALLOWED_HOSTS = your-app-name.onrender.com
CSRF_TRUSTED_ORIGINS = https://your-app-name.onrender.com
```

Replace `your-app-name` with your actual Render service name.

### Step 4: Deploy

Render will automatically:
1. Detect your push to GitHub
2. Install dependencies
3. Run migrations on PostgreSQL
4. Run migrations on SQLite backup
5. Start your application

### Step 5: Verify Deployment

Check Render logs for:
```
✓ PostgreSQL is available - using default database
✓ Migrations completed successfully on 'default'
✓ Migrations completed successfully on 'backup'
```

## Local Development vs Production

### Local Development (Current)
```
DATABASE_URL: Not set
Active Database: SQLite (db.sqlite3)
Fallback: None (not needed)
Command: python manage.py runserver
```

### Production on Render
```
DATABASE_URL: Set from Render
Active Database: PostgreSQL
Fallback: SQLite (db_backup.sqlite3)
Command: gunicorn hrms.wsgi:application
```

## Testing Your Setup

### Test 1: Local Server (Already Working ✅)
```bash
python manage.py runserver
# Should start successfully with SQLite
```

### Test 2: Migration Script
```bash
python migrate_and_sync.py
# Should migrate SQLite backup locally
```

### Test 3: After Deployment
1. Visit your Render URL
2. Test employee management
3. Test attendance tracking
4. Check Render logs for database status

## What Happens When PostgreSQL Fails?

### Automatic Failover Process:
```
1. Request arrives
2. System tries PostgreSQL
3. PostgreSQL unavailable (timeout/error)
4. System automatically switches to SQLite
5. Application continues running
6. User sees no difference
7. Logs show: "PostgreSQL unavailable - falling back to SQLite"
```

### Automatic Recovery:
```
1. PostgreSQL comes back online
2. System detects recovery (every 10 requests)
3. Switches back to PostgreSQL
4. Logs show: "PostgreSQL connection restored"
```

## Important Files

### Configuration Files:
- `hrms/settings.py` - Database configuration
- `hrms/db_router.py` - Automatic failover logic
- `hrms/middleware.py` - Database health monitoring
- `render.yaml` - Deployment configuration

### Documentation:
- `SECURITY_SETUP.md` - Security best practices
- `DATABASE_SETUP.md` - Detailed database guide
- `IMPLEMENTATION_SUMMARY.md` - Technical details
- `.env.example` - Environment variables template

### Scripts:
- `migrate_and_sync.py` - Automatic migration script

## Security Checklist Before Deployment

- [x] No credentials in code
- [x] `.env` in `.gitignore`
- [x] `db_backup.sqlite3` in `.gitignore`
- [x] `render.yaml` uses environment variables
- [x] `.env.example` provided (no real values)
- [ ] Set `DATABASE_URL` in Render (you need to do this)
- [ ] Set `ALLOWED_HOSTS` in Render (you need to do this)
- [ ] Set `CSRF_TRUSTED_ORIGINS` in Render (you need to do this)

## Next Steps

1. **Set Environment Variables in Render**
   - DATABASE_URL (from database)
   - ALLOWED_HOSTS (your domain)
   - CSRF_TRUSTED_ORIGINS (your URL)

2. **Push to GitHub**
   ```bash
   git push origin main
   ```

3. **Monitor Deployment**
   - Watch Render logs
   - Verify migrations run
   - Test application

4. **Verify Everything Works**
   - Add an employee
   - Mark attendance
   - Check data persists

## Need Help?

- Check `SECURITY_SETUP.md` for environment variable setup
- Check `DATABASE_SETUP.md` for database configuration
- Check Render logs for deployment issues
- Verify all environment variables are set correctly

## Summary

✅ **Your code is secure** - No hardcoded credentials
✅ **Local development works** - Using SQLite
✅ **Production ready** - Just need to set environment variables in Render
✅ **Automatic failover** - PostgreSQL → SQLite if needed
✅ **Automatic recovery** - SQLite → PostgreSQL when available

**You're ready to deploy!** Just set the environment variables in Render's dashboard.
