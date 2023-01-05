import asyncio

async def run_get_exchange()->None:
    n = 0
    while True:
        await asyncio.sleep(1)
        print("seconds: ", n)
        n+=1

async def run_bot() -> None:
    n=0
    while True:
        await asyncio.sleep(2)
        print("4seconds !", n)
        n+=1



async def main() -> None:
    bot = asyncio.create_task(run_bot())
    valuta = asyncio.create_task(run_get_exchange())
    await bot
    await valuta

if __name__=="__main__":
    asyncio.run(main())

