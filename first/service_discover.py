from . import db
import re
from collections import defaultdict


def discover():
    keys = db.redis_connection.keys()
    app_keys = db.redis_connection.lrange("web_app", 0, -1)

    app_replica = defaultdict(list)
    alive_replicas = []
    app_prefix = "web_app"
    replica_prefix = "replica"
    sep_char = '_'

    if keys is not None:

        for key in keys:
            if replica_prefix in key:
                # app = re.search(replica_prefix + sep_char + "(.+?)" + sep_char, key).group(1)
                # app_replica[app_prefix + sep_char + app].append(key)
                app_replica["web_app"].append(key)
                alive_replicas.append(key)

        for key, value in app_replica.items():

            for val in value:
                if val not in app_keys:
                    db.redis_connection.lpush("web_app", val)

            for val in app_keys:
                if val not in value:
                    db.redis_connection.lrem(name="web_app", count=0, value=val)

                    # # push all active replicas
                    # db.redis_connection.sadd(key, *value)
                    #
                    # # delete all inactive replicas
                    # app_replicas = db.redis_connection.smembers(key)
                    # for replica in app_replicas:
                    #     if replica not in alive_replicas:
                    #         db.redis_connection.srem(key, replica)