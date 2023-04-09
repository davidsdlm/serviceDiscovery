import redis
from . import db, service_discover
from apscheduler.schedulers.background import BackgroundScheduler


def init_redis(host: str, port: int, password: str):
    if db.redis_connection is None:
        db.redis_connection = redis.Redis(host=host, port=port, db=0, password=password, decode_responses=True)
    else:
        raise


def init_scheduler(interval):
    if db.redis_discover_scheduler is None:
        db.redis_discover_scheduler = BackgroundScheduler(job_defaults={'max_instances': 2})
        db.redis_discover_scheduler.add_job(service_discover.discover, 'interval', seconds=interval)
        db.redis_discover_scheduler.start()
    else:
        raise


def shutdown_scheduler():
    if db.redis_discover_scheduler is not None:
        db.redis_discover_scheduler.shutdown()
    else:
        pass
