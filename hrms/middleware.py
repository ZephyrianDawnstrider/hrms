"""
Database Health Monitoring Middleware
Monitors database connectivity and handles automatic failover
"""
import logging
from django.core.cache import cache
from django.db import connections, DatabaseError

logger = logging.getLogger(__name__)


class DatabaseHealthMiddleware:
    """
    Middleware to monitor database health and log database switches.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check database health before processing request
        self._check_database_health()
        
        response = self.get_response(request)
        return response
    
    def _check_database_health(self):
        """
        Check if PostgreSQL is available and log status changes.
        """
        try:
            conn = connections['default']
            conn.ensure_connection()
            
            # If we were previously on backup, log the recovery
            if cache.get('database_status') == 'backup':
                logger.info("PostgreSQL connection restored - switching back from SQLite")
                cache.set('database_status', 'default', 300)
                cache.delete('active_database')  # Clear router cache to re-check
            
        except DatabaseError as e:
            # PostgreSQL is down, ensure we're using backup
            if cache.get('database_status') != 'backup':
                logger.warning(f"PostgreSQL connection lost - using SQLite backup: {str(e)}")
                cache.set('database_status', 'backup', 300)
                cache.delete('active_database')  # Clear router cache to re-check
    
    def process_exception(self, request, exception):
        """
        Handle database-related exceptions.
        """
        if isinstance(exception, DatabaseError):
            logger.error(f"Database error occurred: {str(exception)}")
            cache.delete('active_database')  # Force router to re-check database
        
        return None
