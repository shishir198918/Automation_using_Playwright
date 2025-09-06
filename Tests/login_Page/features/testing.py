import asyncio
import time 
async def task(name, delay):
    print(f"{name} started")
    time.sleep(delay)
    print(f"{name} finished after {delay}s")

async def main():
    await asyncio.gather(
        task("Task A", 5),
        task("Task B", 5),
    )

asyncio.run(main())
