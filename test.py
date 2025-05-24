import asyncio, time
from redis.asyncio import Redis

async def benchmark(n=10_000):
    r = Redis.from_url("redis://localhost:6379/0", decode_responses=True)
    # warm up
    for _ in range(1_000):
        await r.ping()
    start = time.perf_counter()
    tasks = [r.ping() for _ in range(n)]
    await asyncio.gather(*tasks)
    total = time.perf_counter() - start
    print(f"{n} pings in {total:.2f}s → {n/total:.0f} ops/sec")
    await r.close()

if __name__ == "__main__":
    asyncio.run(benchmark())
