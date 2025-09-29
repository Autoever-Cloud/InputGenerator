# auth_inputgenerator5.py

import time
import random
import sys
import socket
from datetime import datetime, timezone, timedelta
import threading
from prometheus_client import Counter, generate_latest, REGISTRY
from fastapi import FastAPI, Response
import uvicorn

RATE_HACKING_ATTEMPT = 0.1
MIN_INTERVAL, MAX_INTERVAL = 1, 10

# ✅ Prometheus 메트릭 정의
auth_attempts_total = Counter(
    'auth_attempts_total',
    'Total SSH authentication attempts',
    ['result']
)

app = FastAPI()

@app.get("/metrics")
def metrics():
    return Response(generate_latest(REGISTRY), media_type="text/plain")


def generate_single_auth_log(result="success", ip=None):
    """단일 로그를 생성하는 함수"""
    users = ["root", "admin", "kyla", "lnaura", "yes-ee", "guest", "chu", "leeejjju", "hoit"]
    ips = ["104.28.231.109", "10.0.1.100", "211.34.56.78", "192.168.1.1"]
    hostname = socket.gethostname()
    pid = random.randint(10000, 20000)
    ts = datetime.now(timezone(timedelta(hours=9)))

    # IP가 지정되지 않았다면 랜덤 선택
    ip = ip or random.choice(ips)

    if result == "success":
        user = random.choice(users[:-2])  # 성공 로그는 정상 계정만
        message = f"Accepted password for {user} from {ip} port {random.randint(40000, 60000)} ssh2"
    else:
        user = random.choice(users)  # 실패 로그는 모든 계정 가능
        message = f"Failed password for invalid user {user} from {ip} port {random.randint(40000, 60000)} ssh2"

    # 📊 메트릭 업데이트
    auth_attempts_total.labels(result=result).inc()

    return f"{ts} {hostname} sshd[{pid}]: {message}"


def generate_auth_log_batch():
    """
    ✅ 0.1 확률로 동일 IP에서 실패 로그 10개 생성
    ✅ 나머지 경우에는 기존 방식대로 1개 로그 생성
    """
    if random.random() < RATE_HACKING_ATTEMPT:
        # 동일 IP에서 실패 로그 10개 출력
        fixed_ip = random.choice(["104.28.231.109", "10.0.1.100", "211.34.56.78", "192.168.1.1"])
        logs = [generate_single_auth_log(result="failed", ip=fixed_ip) for _ in range(10)]
        return logs
    else:
        # 기존 단일 로그 출력
        result = "success" if random.random() > 0.3 else "failed"
        return [generate_single_auth_log(result=result)]


def log_loop():
    while True:
        time.sleep(random.uniform(MIN_INTERVAL, MAX_INTERVAL))
        logs = generate_auth_log_batch()
        for log in logs:
            print(log)
        sys.stdout.flush()


if __name__ == "__main__":
    threading.Thread(target=log_loop, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=8080)
