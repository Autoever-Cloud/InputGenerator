# memory_inputgenerator3.py

import time
import random
import sys

kernel_timestamp = random.uniform(50000, 60000)

def generate_mce_log():
    """Machine Check Exception (MCE) 하드웨어 에러 로그를 Plaintext로 생성합니다."""
    global kernel_timestamp
    kernel_timestamp += random.uniform(500, 2000)
    ts = kernel_timestamp
    
    return (
        f"[{ts:.6f}] mce: [Hardware Error]: CPU {random.randint(0,7)}: Machine Check: 0 Bank 5: bea0000000000108\n"
        f"[{ts + 0.000011:.6f}] mce: [Hardware Error]: TSC 0 ADDR {random.randint(1,9)}f{random.randint(100,999)}b{random.randint(1000,9999)} MISC {random.randint(1,9)}880000086\n"
        f"[{ts + 0.000021:.6f}] mce: [Hardware Error]: PROCESSOR 0:50654 TIME {int(time.time())} SOCKET 0 APIC 0 microcode 1000140\n"
        f"[{ts + 0.000031:.6f}] mce: [Hardware Error]: Machine Check: Uncorrected ECC error"
    )

if __name__ == "__main__":
    while True:
        # 1분 ~ 5분 사이의 랜덤한 간격으로 매우 드물게 로그 생성
        time.sleep(random.uniform(60, 300))
        log_message = generate_mce_log()
        print(log_message)
        sys.stdout.flush()
