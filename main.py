import asyncio
from enum import Enum
from typing import List
from datetime import timedelta
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor

from aiohttp import ClientTimeout, ClientSession

timeout_seconds = timedelta(seconds=15).total_seconds()

class Result(Enum):
    Accepted = 1
    Rejected = 2

@dataclass
class Payload:
    # TODO дополнить реализацию
    pass


@dataclass
class Address:
    # TODO дополнить реализацию
    pass

@dataclass
class Event:
    recipients: List[Address]
    payload: Payload


async def read_data(executor: ThreadPoolExecutor) -> Event:
    try:
        await asyncio.sleep(1)
    except asyncio.CancelledError:
        raise
    except Exception as e:
        print(f'Error in read_data: {e}')

    recipients = [Address() for _ in range(5)]
    payload = Payload()
    event = Event(recipients, payload)

    return event


async def send_data(dest: Address, payload: Payload) -> Result:
    try:

        # Имитация блокирующей операции отправки

        timeout = ClientTimeout(total=timeout_seconds)

        async with ClientSession(timeout=timeout) as session:

            async with session.request(method='POST', url='http://example.com', data=payload.to_bytes()) as resp:
                status = resp.status
                if status == 200:
                    return Result.Accepted
                elif status == 503:
                    return Result.Rejected
                else:
                    return Result.Rejected

    except asyncio.CancelledError:
        raise
    except Exception as e:
        print(f'Error in send_ {e}')

async def handle_result(result: Result, retriesCount: int, dest: Address, payload: Payload):
    if result == Result.Rejected:
        if retriesCount < 3:
            retriesCount += 1
            await asyncio.sleep(5)
            return await send_data(dest, payload)
        else:
            print('Max retries reached')
            return Result.Rejected
    return result

async def perform_operation() -> None:
    # TODO дополнить реализацию
    pass

# async code run
asyncio.run(perform_operation())