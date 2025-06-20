import aiohttp
import asyncio
import time

N = 100000

async def send_request(session):
    try:
        async with session.post(
            "http://localhost:8080/classic", json={"a": 1, "b": 2, "c": 3}
        ) as response:
            if response.status == 200:
                result = await response.json()
                return result
            else:
                print(
                    f"Request failed with status {response.status}, body: {await response.text()}"
                )
    except Exception as e:
        print(f"Error during request: {e}")


async def main():
    """Основная функция для отправки асинхронных запросов."""
    tasks = []
    async with aiohttp.ClientSession() as session:
        for i in range(N):
            task = asyncio.create_task(send_request(session))
            tasks.append(task)

        # Ожидаем завершения всех задач
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        # Обработка результатов
        for i, response in enumerate(responses):
            if isinstance(response, Exception):
                print(f"Error in request {i + 1}: {response}")


start_time = time.time()
asyncio.run(main())
elapsed_time = time.time() - start_time
print(f"All requests {N} completed in {elapsed_time:.2f} seconds.")
