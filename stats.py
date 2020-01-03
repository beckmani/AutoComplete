import redis
import redis_lock

class StatsServer:

    def __init__(self):
        self.redis_conn = redis.StrictRedis(host='redis', port=6379)
        self._lock = redis_lock.Lock(self.redis_conn, "stat-lock")
        self._lock.acquire()
        self.redis_conn.set('averageRequestHandleTimeMs', 0)
        self.redis_conn.set('requestHandledCount', 0)
        self.redis_conn.set('wordCount', 0)
        self._lock.release()

    def _get_int_value_from_redis(self, key):
        val = int(self.redis_conn.get(key).decode('utf-8'))
        return val

    def get_stats(self):
        self._lock.acquire()
        wc = self._get_int_value_from_redis('wordCount')
        req = self._get_int_value_from_redis('requestHandledCount')
        avg = self._get_int_value_from_redis('averageRequestHandleTimeMs')
        self._lock.release()
        return {'wordCount': wc, 'requestHandledCount': req, 'averageRequestHandleTimeMs': avg}

    def update_word_count(self, words):
        self._lock.acquire()
        self.redis_conn.set('wordCount', words)
        self._lock.release()

    def update_request_stats(self, duration):
        self._lock.acquire()
        avg = self._get_int_value_from_redis('averageRequestHandleTimeMs')
        req = self._get_int_value_from_redis('requestHandledCount')
        self.redis_conn.set('requestHandledCount', req+1)

        moving_avg = int(((req * avg) + duration) / (req+1))
        self.redis_conn.set('averageRequestHandleTimeMs', moving_avg)
        self._lock.release()

