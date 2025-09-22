# memory_inputgenerator2.py

import time
import random
import sys

kernel_timestamp = random.uniform(40000, 50000)

def generate_oom_killer_log():
    """Out of Memory (OOM) Killer 로그를 Plaintext로 생성합니다."""
    global kernel_timestamp
    kernel_timestamp += random.uniform(100, 500)
    ts = kernel_timestamp
    pid = random.randint(10000, 30000)
    
    return (
        f"[{ts:.6f}] Out of memory: Killed process {pid} (java) total-vm:{random.randint(2000000,4000000)}kB, anon-rss:{random.randint(1800000,2000000)}kB\n"
        f"[{ts + 0.000007:.6f}] CPU: {random.randint(0,7)} PID: {pid} Comm: java Not tainted 5.15.0-107-generic #117-Ubuntu\n"
        f"[{ts + 0.000027:.6f}] oom_reaper: reaped process {pid} (java), now anon-rss:0"
    )

if __name__ == "__main__":
    while True:
        # 30초 ~ 2분 사이의 랜덤한 간격으로 드물게 로그 생성
        time.sleep(random.uniform(30, 120))
        log_message = generate_oom_killer_log()
        print(log_message)
        sys.stdout.flush()
