"""Scan vs hash index: correctness check, then timings and memory.

Usage: python3 bench.py [n_writes] [n_distinct_keys]
"""

import os
import random
import sys
import time
import tracemalloc

from hash_db import HashIndexDB

N_WRITES = int(sys.argv[1]) if len(sys.argv) > 1 else 200_000
N_KEYS = int(sys.argv[2]) if len(sys.argv) > 2 else 20_000
N_SCAN_READS = 50      # scans are slow; keep this small
N_INDEX_READS = 50_000
PATH = "bench.db"


def timed(fn):
    start = time.perf_counter()
    fn()
    return time.perf_counter() - start


if os.path.exists(PATH):
    os.remove(PATH)

random.seed(42)
db = HashIndexDB(PATH)
latest = {}

# 1. Writes: N_WRITES appends spread over N_KEYS keys (so most keys get overwritten).
def do_writes():
    for i in range(N_WRITES):
        key = f"user_{random.randrange(N_KEYS)}"
        value = f'{{"name": "n{i}", "visits": {i}}}'
        db.set(key, value)
        latest[key] = value

t_write = timed(do_writes)

# 2. Correctness: index must agree with the scan and with what we last wrote.
sample = random.sample(sorted(latest), min(N_SCAN_READS, len(latest)))
for key in sample:
    assert db.get(key) == latest[key] == db.scan_get(key), f"mismatch for {key}"
assert db.get("no_such_key") is None
print("correctness: OK (index == scan == last write)\n")

# 3. Reads.
t_scan = timed(lambda: [db.scan_get(k) for k in sample])
keys = list(latest)
t_index = timed(lambda: [db.get(random.choice(keys)) for _ in range(N_INDEX_READS)])

# 4. Restart: the dict is gone, rebuild from disk.
db.close()
tracemalloc.start()
t_rebuild = timed(lambda: globals().__setitem__("db", HashIndexDB(PATH)))
_, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
assert all(db.get(k) == latest[k] for k in sample), "index wrong after restart"

size = db.file_size()
print(f"writes:          {N_WRITES:>10,}  in {t_write:.2f}s  ({N_WRITES / t_write:,.0f}/s)")
print(f"scan get:        {t_scan / len(sample) * 1e3:>10.2f} ms per read")
print(f"index get:       {t_index / N_INDEX_READS * 1e6:>10.2f} us per read")
print(f"speedup:         {(t_scan / len(sample)) / (t_index / N_INDEX_READS):>10,.0f}x")
print(f"rebuild on boot: {t_rebuild:>10.2f} s")
print(f"index entries:   {len(db.index):>10,}")
print(f"index RAM (~):   {peak / 1e6:>10.1f} MB")
print(f"file on disk:    {size / 1e6:>10.1f} MB  ({N_WRITES:,} lines for {len(db.index):,} live keys)")
db.close()
