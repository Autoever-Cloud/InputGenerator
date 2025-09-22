import json
import random
import socket
import time

MIN_TERM = 0.5
MAX_TERM = 2.0


# syslog priority 매핑 (참고용, JSON에는 정수만 저장)
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

# priority별 발생 가중치
PRIORITY_WEIGHTS = {
    0: 1,   # emerg
    1: 2,   # alert
    2: 3,   # crit
    3: 5,   # err
    4: 10,  # warning
    5: 15,  # notice
    6: 30,  # info
    7: 10   # debug
}

# priority별 샘플 메시지 풀
MESSAGE_TEMPLATES = {
    0: [
        "Kernel panic - not syncing: Fatal exception",
        "BUG: unable to handle kernel NULL pointer dereference",
        "VFS: Unable to mount root fs on unknown-block(0,0)"
    ],
    1: [
        "System halted due to unrecoverable error",
        "Critical security violation detected: dropping to emergency shell",
        "Audit: failed login attempts exceeded threshold"
    ],
    2: [
        "CPU overheating detected, shutting down core",
        "Filesystem corruption detected on /dev/sda1",
        "RAID array degraded: disk failure reported"
    ],
    3: [
        "Out of memory: Kill process 1234 (java) score 987",
        "I/O error on device sda, sector 123456",
        "EXT4-fs error (device sdb): ext4_find_entry:1309: inode #12345"
    ],
    4: [
        "eth0: packet collision detected",
        "Disk warning: SMART status indicates impending failure",
        "USB disconnect: device 2-1.3 unplugged"
    ],
    5: [
        "systemd: Started User Manager for UID 1000",
        "systemd: Stopping Session c1 of user root",
        "audit: user root logged in via ssh"
    ],
    6: [
        "usb 1-1: new high-speed USB device detected",
        "systemd: Reached target Multi-User System",
        "ACPI: Power Button pressed",
        "cron: job 'backup.sh' completed successfully"
    ],
    7: [
        "debug: entering scheduler tick",
        "net: tcp connection setup completed",
        "mm: page allocation succeeded",
        "driver: probing device on bus pci0000:00"
    ]
}

def generate_log(seq):
    # priority 확률적 선택
    priorities = list(PRIORITY_WEIGHTS.keys())
    weights = list(PRIORITY_WEIGHTS.values())
    priority = random.choices(priorities, weights=weights, k=1)[0]

    # 메시지 랜덤 선택
    message = random.choice(MESSAGE_TEMPLATES[priority])

    # JSON 로그 구조
    log = {
        "priority": priority,
        "facility": 0,  # 커널은 항상 0
        "seq": seq,
        "timestamp": f"{time.monotonic():.6f}",
        "message": message,
        "host": socket.gethostname()
    }

    return log


if __name__ == "__main__":
    seq = 0
    while True:
        log = generate_log(seq)
        print(json.dumps(log, ensure_ascii=False))
        seq += 1
        time.sleep(random.uniform(MIN_TERM, MAX_TERM))  # 0.5~2초 간격 출력
