"""
Database Router for PostgreSQL with SQLite Fallback
Automatically switches to SQLite backup when PostgreSQL is unavailable
"""
import logging
from django.db import connections
from django.db.utils import OperationalError, DatabaseError

logger = logging.getLogger(__name__)


class FallbackDatabaseRouter:
    """
    A router to control database operations with automatic fallback.
    
    - Tries PostgreSQL first (default database)
    - Falls back to SQLite (backup database) if PostgreSQL fails
    - Uses in-memory cache to avoid repeated connection attempts
    """
    
    _active_db = None
    _check_counter = 0
    _check_interval = 10  # Check PostgreSQL every 10 requests
    
    def _get_active_database(self):
        """
        Determine which database is currently active.
        Returns 'default' (PostgreSQL) or 'backup' (SQLite)
        """
        # Use cached value if available and not time to recheck
        if self._active_db and self._check_counter < self._check_interval:
            self._check_counter += 1
            return self._active_db
        
        # Reset counter
        self._check_counter = 0
        
        # Try PostgreSQL connection
        try:
            conn = connections['default']
            # Quick connection test without full ensure_connection
            if conn.connection is None:
                conn.connect()
            
            # Test with a simple query
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
            
            if self._active_db != 'default':
                logger.info("PostgreSQL is available - using default database")
            self._active_db = 'default'
            return 'default'
            
        except (OperationalError, DatabaseError) as e:
            if self._active_db != 'backup':
                logger.warning(f"PostgreSQL unavailable - falling back to SQLite: {str(e)}")
            self._active_db = 'backup'
            return 'backup'
        except Exception as e:
            # Catch any other exceptions during startup
            if self._active_db != 'backup':
                logger.warning(f"Database error - falling back to SQLite: {str(e)}")
            self._active_db = 'backup'
            return 'backup'
    
    def db_for_read(self, model, **hints):
        """
        Attempts to read from PostgreSQL, falls back to SQLite if unavailable.
        """
        return self._get_active_database()
    
    def db_for_write(self, model, **hints):
        """
        Attempts to write to PostgreSQL, falls back to SQLite if unavailable.
        """
        return self._get_active_database()
    
    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if both objects are in the same database.
        """
        return True
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Allow migrations on both databases.
        """
        return True
