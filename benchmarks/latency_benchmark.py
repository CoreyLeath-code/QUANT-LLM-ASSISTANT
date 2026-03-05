import requests
import time

def benchmark():
    start = time.time()
    for _ in range(100):
        requests.post("http://localhost:8000/query", json={"question":"What is inflation?"})
    print("Average latency:", (time.time()-start)/100)
