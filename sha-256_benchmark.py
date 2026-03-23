import time
import statistics
import hashlib

sizes = [8,64,512,4096,32768,262144,2097152]

def sha256_hash(data):
    return hashlib.sha256(data).digest()

for s in sizes:

    with open(f"ficheiro_{s}.txt","rb") as f:
        data = f.read()

    times = []

    for _ in range(30):   # repetir várias vezes

        start = time.perf_counter()
        sha256_hash(data)
        times.append(time.perf_counter() - start)

    mean = statistics.mean(times) * 1e6
    std = statistics.stdev(times) * 1e6

    print(s, "SHA:", mean, "±", std)