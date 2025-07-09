import os, json
import redis

redis_conn = redis.Redis.from_url(os.getenv("REDIS_BROKER"))

def publish_alert_to_redis(alert: dict):
    redis_conn.publish(os.getenv("ALERT_CHANNEL", "alert_notifications"), json.dumps(alert))
