# login_inputgenerator5.py

import time
import random
import sys
from datetime import datetime

def generate_auth_log():
    """auth.log (sshd)와 유사한 포맷의 로그를 생성합니다."""
    
    users = ["root", "admin", "kyla", "dev", "attacker", "guest"]
    ips = ["104.28.231.109", "10.0.1.100", "211.34.56.78", "192.168.1.1"]
    hostname = "prod-bastion-01"
    pid = random.randint(10000, 20000)
    ts = datetime.now().strftime('%b %d %H:%M:%S')

    # 70%는 성공, 30%는 실패
    if random.random() > 0.3:
        user = random.choice(users[:-2]) # attacker, guest 제외
        message = f"Accepted password for {user} from {random.choice(ips)} port {random.randint(40000, 60000)} ssh2"
    else:
        user = random.choice(users)
        message = f"Failed password for invalid user {user} from {random.choice(ips)} port {random.randint(40000, 60000)} ssh2"
        
    return f"{ts} {hostname} sshd[{pid}]: {message}"

if __name__ == "__main__":
    while True:
        # 1초 ~ 10초 사이의 랜덤한 간격으로 로그 생성
        time.sleep(random.uniform(1.0, 10.0))
        log_message = generate_auth_log()
        print(log_message)
        sys.stdout.flush()
