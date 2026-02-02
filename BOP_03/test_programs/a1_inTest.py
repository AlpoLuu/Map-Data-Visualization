import sys

for i in range(5):
    sys.stdout.write(f"Hello, Message, {i}\n")

sys.stdout.flush()


#flush in for loop
    # messages 0,1,...,4
#flush outside for loop
    # messages 0,1,...,4