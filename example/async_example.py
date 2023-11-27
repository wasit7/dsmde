import asyncio
import aiohttp
import pandas as pd

async def timer(name, seconds):
    for i in range(seconds):
        await asyncio.sleep(1)
        print(f"Timer {name}: {i + 1} second(s) passed")
    print(f'Timer {name}: finished!')

async def main():
    # Running two timers concurrently
    await asyncio.gather(
        timer("A", 5),  # Timer A for 5 seconds
        timer("B", 3)   # Timer B for 3 seconds
    )
    
if __name__ == "__main__":
    asyncio.run(main())