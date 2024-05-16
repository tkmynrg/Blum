from utils.core import create_sessions
from utils.telegram import Accounts
from utils.blum import Start
import asyncio
from itertools import zip_longest
from utils.core import get_all_lines
import argparse


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--action', type=int, help='Action to perform')
    action = parser.parse_args().action

    if action == 1:
        await create_sessions()

    if action == 2:
        accounts = await Accounts().get_accounts()
        proxys = get_all_lines("data/proxy.txt")

        tasks = []
        for thread, (account, proxy) in enumerate(zip_longest(accounts, proxys)):
            if not account: break
            tasks.append(asyncio.create_task(Start(account=account, thread=thread, proxy=proxy).main()))

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
