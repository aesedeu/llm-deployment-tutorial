import asyncio
import aiohttp
import time
import random
import numpy as np
import signal

active_requests = 0
stop_event = asyncio.Event()

# Обработка Ctrl+C
def shutdown_handler():
    print("\n⛔ Остановка по Ctrl+C...")
    stop_event.set()

signal.signal(signal.SIGINT, lambda s, f: shutdown_handler())

async def fetch_stream(session, idx):
    global active_requests
    url = "http://localhost:8001/stream"
    headers = {"Content-Type": "application/json"}
    payload = {
        "message": "What are the symptoms of hypertension?",
        "model": "Qwen/Qwen2.5-0.5B-Instruct",
        "temperature": 1.0,
        "max_tokens": 300
    }

    active_requests += 1
    print(f"🚀 Запущен запрос {idx}. Активных запросов: {active_requests}")
    start_time = time.perf_counter()
    result_text = ""

    try:
        async with session.post(url, json=payload) as resp:
            async for chunk in resp.content.iter_chunked(1024):
                result_text += chunk.decode("utf-8")
    except Exception as e:
        print(f"❌ Ошибка в запросе {idx}: {e}")
    finally:
        elapsed = time.perf_counter() - start_time
        active_requests -= 1
        print(f"✅ Запрос {idx} завершён за {elapsed:.2f} сек\nСгенерировано токенов: {len(result_text)}\nОтвет: {result_text[:80]}...\n")

async def generator():
    idx = 1
    async with aiohttp.ClientSession() as session:
        while not stop_event.is_set():
            asyncio.create_task(fetch_stream(session, idx))
            idx += 1
            await asyncio.sleep(np.random.randn() * 7)

async def main():
    print("🚧 Начинаем генерацию запросов (нажмите Ctrl+C для остановки)...")
    await generator()

if __name__ == "__main__":
    asyncio.run(main())
