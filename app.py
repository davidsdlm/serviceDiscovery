import sys

from first import init_redis, init_scheduler, shutdown_scheduler
import os
import signal
import time


def handler(sig, frame):
    if sig == signal.SIGINT or sig == signal.SIGTERM:
        shutdown_scheduler()
        sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":

    REDIS_HOST = os.environ['REDIS_HOST']
    REDIS_PORT = os.environ['REDIS_PORT']
    REDIS_PORT = int(REDIS_PORT)
    REDIS_PASSWORD = os.environ['REDIS_PASSWORD']
    # 8001 - insight
    init_redis(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)

    SERVICE_DISCOVER_INTERVAL = os.environ['SERVICE_DISCOVER_INTERVAL']
    SERVICE_DISCOVER_INTERVAL = int(SERVICE_DISCOVER_INTERVAL)
    init_scheduler(SERVICE_DISCOVER_INTERVAL)

    signal.signal(signal.SIGINT, handler)
    while True:
        time.sleep(20)
