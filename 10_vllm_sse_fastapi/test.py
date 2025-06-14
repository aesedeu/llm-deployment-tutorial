import asyncio
import aiohttp
import time

N = 30

async def fetch_stream(session, idx):
    url = "http://localhost:8001/stream"
    headers = {"Content-Type": "application/json"}
    payload = {
        "message": "What is the treatment for high blood pressure?",
        "model": "Qwen/Qwen2.5-0.5B-Instruct",
        "temperature": 1.0,
        "max_tokens": 200
    }

    start_time = time.perf_counter()
    result_text = ""

    try:
        async with session.post(url, json=payload) as resp:
            if resp.status != 200:
                print(f"❌ Запрос {idx} вернул статус {resp.status}")
                return

            async for chunk in resp.content.iter_chunked(1024):
                result_text += chunk.decode("utf-8")

    except Exception as e:
        print(f"❌ Ошибка в запросе {idx}: {e}")
        return

    elapsed = time.perf_counter() - start_time
    print(f"✅ Запрос {idx} выполнен за {elapsed:.2f} сек\nСгенерировано токенов: {len(result_text)}\nОтвет: {result_text[:50]}...\n")


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_stream(session, i + 1) for i in range(N)]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
