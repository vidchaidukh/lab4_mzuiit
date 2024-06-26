from prometheus_client import start_http_server, Counter, Gauge
import time
import random

# Ініціалізація метрик
REQUEST_COUNT = Counter('request_count', 'Total request count')

# Create a gauge metric to measure system memory usage
memory_usage = Gauge('memory_usage_in_bytes', 'System Memory Usage')

   
def process_request():
    REQUEST_COUNT.inc()
    time.sleep(random.random())

if __name__ == '__main__':
    start_http_server(9091)
    while True:
        process_request()

