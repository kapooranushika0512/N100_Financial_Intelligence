import time
from concurrent.futures import ThreadPoolExecutor

import requests

URL = "http://127.0.0.1:8000/api/v1/screener/"


def hit_api(i):
    start = time.perf_counter()

    response = requests.get(URL)

    elapsed = time.perf_counter() - start

    return {"Request": i, "Status": response.status_code, "Time": elapsed}


start = time.perf_counter()

with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(hit_api, range(1, 11)))

total = time.perf_counter() - start

print("\n========= RESULTS =========\n")

for r in results:
    print(
        f"Request {r['Request']:2d} | "
        f"Status {r['Status']} | "
        f"{r['Time']:.3f} sec"
    )

print("\n===========================\n")

print(f"Total Time : {total:.3f} sec")
print(f"Average    : {sum(r['Time'] for r in results)/10:.3f} sec")
print(f"Maximum    : {max(r['Time'] for r in results):.3f} sec")
print(f"Minimum    : {min(r['Time'] for r in results):.3f} sec")

if total < 10:
    print("\n✅ PASS - Completed within 10 seconds")
else:
    print("\n❌ FAIL - Took longer than 10 seconds")
