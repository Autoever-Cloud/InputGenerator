# service_inputgenerator1.py

import json
import time
import random
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

def generate_http_request_log():
    """HTTP 요청에 대한 JSON 로그를 생성합니다."""
    
    apis = ["/api/v1/users", "/api/v1/products", "/api/v1/orders", "/health"]
    
    # 95% 확률로 200, 3% 확률로 404, 2% 확률로 502 상태 코드 생성
    status_code = random.choices(
        population=[200, 404, 502], 
        weights=[0.95, 0.03, 0.02], 
        k=1)[0]

    log_entry = {
        "timestamp" = datetime.now(ZoneInfo("Asia/Seoul")).isoformat(),
        "sourceIP": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
        "API": random.choice(apis),
        "result": status_code
    }
    return log_entry

if __name__ == "__main__":
    while True:
        time.sleep(random.uniform(1.0, 3.0)) # 1~3초 간격으로 로그 생성
        log = generate_http_request_log()
        print(json.dumps(log))
        sys.stdout.flush()
