import time
import asyncio

now = lambda : time.time()



async def worker():
    print('Start worker')

    while True:
        start = now()
        await asyncio.sleep(1)

def main():
    asyncio.ensure_future(worker())
    asyncio.ensure_future(worker())

    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    except KeyboardInterrupt as e:
        print(asyncio.gather(*asyncio.Task.all_tasks()).cancel())
        loop.stop()
        loop.run_forever()
    finally:
        loop.close()

if __name__ == '__main__':
    main()