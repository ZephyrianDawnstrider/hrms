#!/usr/bin/env python
"""
Migration and Database Sync Script
Runs migrations on both PostgreSQL and SQLite databases
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from django.core.management import call_command
from django.db import connections
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def migrate_database(database_name):
    """Run migrations on a specific database"""
    try:
        logger.info(f"Running migrations on '{database_name}' database...")
        call_command('migrate', '--database', database_name, verbosity=1)
        logger.info(f"✓ Migrations completed successfully on '{database_name}'")
        return True
    except Exception as e:
        logger.error(f"✗ Migration failed on '{database_name}': {str(e)}")
        return False


def check_database_connection(database_name):
    """Check if database connection is available"""
    try:
        conn = connections[database_name]
        conn.ensure_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
        logger.info(f"✓ Database '{database_name}' is accessible")
        return True
    except Exception as e:
        logger.warning(f"✗ Database '{database_name}' is not accessible: {str(e)}")
        return False


def main():
    """Main migration script"""
    logger.info("=" * 60)
    logger.info("HRMS Database Migration Script")
    logger.info("=" * 60)
    
    # Check PostgreSQL connection
    postgres_available = check_database_connection('default')
    
    # Check SQLite connection
    sqlite_available = check_database_connection('backup')
    
    logger.info("\n" + "=" * 60)
    logger.info("Running Migrations")
    logger.info("=" * 60)
    
    # Migrate PostgreSQL if available
    if postgres_available:
        migrate_database('default')
    else:
        logger.warning("Skipping PostgreSQL migrations - database not accessible")
    
    # Always migrate SQLite backup
    if sqlite_available:
        migrate_database('backup')
    else:
        logger.error("SQLite backup database is not accessible!")
    
    logger.info("\n" + "=" * 60)
    logger.info("Migration Summary")
    logger.info("=" * 60)
    logger.info(f"PostgreSQL (default): {'✓ Ready' if postgres_available else '✗ Unavailable'}")
    logger.info(f"SQLite (backup): {'✓ Ready' if sqlite_available else '✗ Unavailable'}")
    logger.info("=" * 60)
    
    if not postgres_available and not sqlite_available:
        logger.error("CRITICAL: No databases are available!")
        sys.exit(1)
    
    logger.info("\n✓ Migration script completed successfully")


if __name__ == '__main__':
    main()
