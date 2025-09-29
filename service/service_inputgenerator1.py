# service_inputgenerator1.py

import json
import time
import random
import sys
from datetime import datetime, timezone, timedelta
from prometheus_client import Counter, Histogram, generate_latest
from fastapi import FastAPI, Response
import threading
import uvicorn

MAX_TERM, MIN_TERM = 1, 3
RATE_SUCCESS, RATE_WARN, RATE_ERR = 0.95, 0.03, 0.02

# ✅ Prometheus 메트릭 정의
http_requests_total = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['status', 'api']
)

http_request_latency_seconds = Histogram(
    'http_request_latency_seconds',
    'HTTP request latency in seconds',
    ['api']
)

app = FastAPI()

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")


def generate_http_request_log():
    """HTTP 요청 로그 생성 + 메트릭 업데이트"""
    apis = ["/api/v1/users", "/api/v1/products", "/api/v1/orders", "/health"]
    status_code = random.choices([200, 404, 502], weights=[RATE_SUCCESS, RATE_WARN, RATE_ERR])[0]
    api = random.choice(apis)

    # 📊 메트릭 업데이트
    http_requests_total.labels(status=str(status_code), api=api).inc()
    with http_request_latency_seconds.labels(api=api).time():
        time.sleep(random.uniform(0.05, 0.2))  # 가짜 처리 시간

    log_entry = {
        "timestamp": datetime.now(timezone(timedelta(hours=9))).isoformat(),
        "sourceIP": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
        "API": api,
        "result": status_code
    }
    return log_entry


def log_loop():
    while True:
        time.sleep(random.uniform(MAX_TERM, MIN_TERM))
        log = generate_http_request_log()
        print(json.dumps(log))
        sys.stdout.flush()


if __name__ == "__main__":
    threading.Thread(target=log_loop, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=8080)
