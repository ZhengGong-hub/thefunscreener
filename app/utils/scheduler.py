import asyncio
import logging
import threading
import time
from datetime import datetime, timedelta

from app.tasks.market_data_updater import run_daily_update

logger = logging.getLogger(__name__)


class DailyTaskScheduler:
    """Scheduler for running daily tasks."""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DailyTaskScheduler, cls).__new__(cls)
                cls._instance._initialized = False
                cls._instance._running = False
                cls._instance._task = None
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self._running = False
        self._task = None
        self._target_hour = 0  # Run at midnight UTC by default
        self._target_minute = 0
    
    def start(self, target_hour: int = 0, target_minute: int = 0):
        """
        Start the scheduler.
        
        Args:
            target_hour: Hour of the day to run (0-23)
            target_minute: Minute of the hour to run (0-59)
        """
        with self._lock:
            if self._running:
                logger.warning("Scheduler is already running")
                return
            
            self._target_hour = target_hour
            self._target_minute = target_minute
            self._running = True
            
            # Start the scheduler as a background task
            self._task = asyncio.create_task(self._schedule_loop())
            logger.info(f"Scheduler started, will run daily at {target_hour:02d}:{target_minute:02d} UTC")
    
    def stop(self):
        """Stop the scheduler."""
        with self._lock:
            if not self._running:
                logger.warning("Scheduler is not running")
                return
            
            self._running = False
            if self._task:
                self._task.cancel()
            logger.info("Scheduler stopped")
    
    async def _schedule_loop(self):
        """Main scheduling loop."""
        try:
            while self._running:
                try:
                    # Calculate time until next run
                    now = datetime.utcnow()
                    target = now.replace(
                        hour=self._target_hour,
                        minute=self._target_minute,
                        second=0,
                        microsecond=0
                    )
                    
                    # If we've already passed the target time today, schedule for tomorrow
                    if now >= target:
                        target = target + timedelta(days=1)
                    
                    # Calculate seconds until next run
                    delay = (target - now).total_seconds()
                    
                    logger.info(f"Next scheduled run in {delay/3600:.2f} hours")
                    await asyncio.sleep(delay)
                    
                    # Run the task
                    if self._running:  # Check again in case we were stopped during sleep
                        logger.info("Running scheduled task")
                        # Run in a thread to avoid blocking the event loop
                        loop = asyncio.get_event_loop()
                        await loop.run_in_executor(None, run_daily_update)
                        logger.info("Scheduled task completed")
                        
                except asyncio.CancelledError:
                    logger.info("Scheduler task cancelled")
                    break
                except Exception as e:
                    logger.error(f"Error in scheduler loop: {e}")
                    # Sleep a bit before retrying to avoid thrashing
                    await asyncio.sleep(60)
        
        finally:
            self._running = False
            logger.info("Scheduler stopped")


# Singleton instance
scheduler = DailyTaskScheduler() 