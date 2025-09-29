# kmsg_inputgenerator6.py

import json
import random
import socket
import time
import sys
import threading
from prometheus_client import Counter, generate_latest, REGISTRY
from fastapi import FastAPI, Response
import uvicorn

MIN_TERM = 0.5
MAX_TERM = 2.0


# ✅ Prometheus 메트릭 정의
kmsg_total = Counter(
    'kmsg_total',
    'Total number of kernel/system logs generated',
    ['priority']
)
PRIORITY_MAP = {
    0: "emerg",
    1: "alert",
    2: "crit",
    3: "err",
    4: "warning",
    5: "notice",
    6: "info",
    7: "debug"
}

PRIORITY_WEIGHTS = {
    0: 1, 1: 2, 2: 3, 3: 5, 4: 10, 5: 15, 6: 30, 7: 10
}

MESSAGE_TEMPLATES = {
    0: ["Kernel panic - not syncing: Fatal exception", "BUG: unable to handle kernel NULL pointer dereference"],
    1: ["System halted due to unrecoverable error", "Critical security violation detected"],
    2: ["CPU overheating detected, shutting down core", "Filesystem corruption detected"],
    3: ["Out of memory: Kill process 1234 (java)", "I/O error on device sda, sector 123456"],
    4: ["eth0: packet collision detected", "Disk warning: SMART status indicates impending failure"],
    5: ["systemd: Started User Manager for UID 1000", "audit: user root logged in via ssh"],
    6: ["usb 1-1: new high-speed USB device detected", "cron: job 'backup.sh' completed successfully"],
    7: ["debug: entering scheduler tick", "net: tcp connection setup completed"]
}

app = FastAPI()

@app.get("/metrics")
def metrics():
    return Response(generate_latest(REGISTRY), media_type="text/plain")


def generate_log(seq):
    priority = random.choices(list(PRIORITY_WEIGHTS.keys()), weights=PRIORITY_WEIGHTS.values())[0]
    message = random.choice(MESSAGE_TEMPLATES[priority])

    # 📊 메트릭 업데이트
    kmsg_total.labels(priority=PRIORITY_MAP[priority]).inc()

    log = {
        "priority": priority,
        "facility": 0,
        "seq": seq,
        "timestamp": f"{time.monotonic():.6f}",
        "message": message,
        "host": socket.gethostname()
    }
    return log


def log_loop():
    seq = 0
    while True:
        log = generate_log(seq)
        print(json.dumps(log, ensure_ascii=False))
        sys.stdout.flush()
        seq += 1
        time.sleep(random.uniform(MIN_TERM, MAX_TERM))


if __name__ == "__main__":
    threading.Thread(target=log_loop, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=8080)
