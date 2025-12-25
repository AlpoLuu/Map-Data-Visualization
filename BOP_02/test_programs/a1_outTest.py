import sys

for line in sys.stdin:
    # line includes the newline character
    processed = line.strip().upper()
    print(f"Received: {processed}")