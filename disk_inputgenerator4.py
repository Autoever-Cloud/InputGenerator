# disk_inputgenerator4.py

import time
import random
import sys

kernel_timestamp = random.uniform(70000, 80000)

def generate_disk_log():
    """디스크 I/O 에러 또는 SATA 연결 문제 로그를 Plaintext로 생성합니다."""
    global kernel_timestamp
    kernel_timestamp += random.uniform(20, 300)
    ts = kernel_timestamp

    if random.random() > 0.3: # I/O 에러가 더 자주 발생하도록
        sector = random.randint(10000000, 99999999)
        return (
            f"[{ts:.6f}] sd 0:0:0:0: [sda] tag#{random.randint(0,31)} FAILED Result: hostbyte=DID_OK driverbyte=DRIVER_SENSE\n"
            f"[{ts + 0.000005:.6f}] sd 0:0:0:0: [sda] Sense Key : Medium Error [current]\n"
            f"[{ts + 0.000010:.6f}] sd 0:0:0:0: [sda] Add. Sense: Unrecovered read error - auto reallocate failed\n"
            f"[{ts + 0.000015:.6f}] blk_update_request: I/O error, dev sda, sector {sector}"
        )
    else:
        return (
            f"[{ts:.6f}] ata1: SATA link down (SStatus 0 SControl 300)\n"
            f"[{ts + 0.111111:.6f}] ata1.00: disabled"
        )

if __name__ == "__main__":
    while True:
        # 15초 ~ 1분 사이의 랜덤한 간격으로 로그 생성
        time.sleep(random.uniform(15, 60))
        log_message = generate_disk_log()
        print(log_message)
        sys.stdout.flush()
