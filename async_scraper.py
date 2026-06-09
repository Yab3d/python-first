import asyncio
import aiohttp
import json
import time
from dataclasses import dataclass, asdict


@dataclass
class ScrapeResult:
    url: str
    status: int | None
    title: str | None
    elapsed_ms: float
    error: str | None = None


async def fetch_one(
    session: aiohttp.ClientSession,
    url: str,
    semaphore: asyncio.Semaphore,
    retries: int = 3,
) -> ScrapeResult:
    async with semaphore:          
        for attempt in range(1, retries + 1):
            start = time.monotonic()
            try:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    elapsed = (time.monotonic() - start) * 1000
                    text = await resp.text()

                   
                    title = None
                    if "<title>" in text:
                        start_idx = text.index("<title>") + 7
                        end_idx = text.index("</title>", start_idx)
                        title = text[start_idx:end_idx].strip()

                    return ScrapeResult(
                        url=url,
                        status=resp.status,
                        title=title,
                        elapsed_ms=round(elapsed, 2),
                    )

            except asyncio.TimeoutError:
                if attempt == retries:
                    return ScrapeResult(url=url, status=None, title=None,
                                        elapsed_ms=0, error="Timeout")
                await asyncio.sleep(2 ** attempt) 

            except aiohttp.ClientError as e:
                if attempt == retries:
                    return ScrapeResult(url=url, status=None, title=None,
                                        elapsed_ms=0, error=str(e))
                await asyncio.sleep(2 ** attempt)


async def scrape_all(urls: list[str], concurrency: int = 10) -> list[ScrapeResult]:
    semaphore = asyncio.Semaphore(concurrency)    

    async with aiohttp.ClientSession(headers={
        "User-Agent": "Mozilla/5.0 (educational scraper)"
    }) as session:
        tasks = [fetch_one(session, url, semaphore) for url in urls]

        results = []
        completed = 0
        for coro in asyncio.as_completed(tasks):
            result = await coro
            completed += 1
            status = result.status or "ERR"
            print(f"[{completed}/{len(urls)}] {status} — {result.url[:50]}")
            results.append(result)

    return results


def save_results(results: list[ScrapeResult], output_file: str = "results.json"):
    data = [asdict(r) for r in results]
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)

    successful = sum(1 for r in results if r.error is None)
    print(f"\n{'='*40}")
    print(f"Total:      {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed:     {len(results) - successful}")
    avg_ms = sum(r.elapsed_ms for r in results if r.error is None) / max(successful, 1)
    print(f"Avg time:   {avg_ms:.0f}ms")
    print(f"Saved to:   {output_file}")


if __name__ == "__main__":
    base = "https://jsonplaceholder.typicode.com"
    urls = (
        [f"{base}/posts/{i}" for i in range(1, 21)] +
        [f"{base}/users/{i}" for i in range(1, 11)] +
        [f"{base}/todos/{i}" for i in range(1, 21)]
    )

    start = time.time()
    results = asyncio.run(scrape_all(urls, concurrency=10))
    total_time = time.time() - start

    print(f"\nAll {len(urls)} requests in {total_time:.2f}s")
    save_results(results)