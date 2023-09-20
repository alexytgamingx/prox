import sys
import aiohttp
import asyncio
import random
import os
import socket
import time
import re
from Dickscord import Style as fore
from typing import List, Union


class ProxyChecker:
    def __init__(self):
        self.client_timeout: int = 5
        self.endpoint: str = "http://ip-api.com/json/?fields=8217"
        self.country_list_usa: List[str] = ["United States"]
        self.country_list_eu: List[str] = [
            "Albania",
            "Andorra",
            "Austria",
            "Belarus",
            "Belgium",
            "Bosnia and Herzegovina",
            "Bulgaria",
            "Croatia",
            "Cyprus",
            "Czech Republic",
            "Denmark",
            "Estonia",
            "Finland",
            "France",
            "Germany",
            "Greece",
            "Hungary",
            "Iceland",
            "Ireland",
            "Italy",
            "Kosovo",
            "Latvia",
            "Liechtenstein",
            "Lithuania",
            "Luxembourg",
            "Malta",
            "Moldova",
            "Monaco",
            "Montenegro",
            "Netherlands",
            "North Macedonia",
            "Norway",
            "Poland",
            "Portugal",
            "Romania",
            "Russia",
            "San Marino",
            "Serbia",
            "Slovakia",
            "Slovenia",
            "Spain",
            "Sweden",
            "Switzerland",
            "Ukraine",
            "United Kingdom",
            "Vatican City",
        ]
        self.proxy_scraping_list_path: str = "proxy_sources.txt"
        self.scraped_proxies: List[str] = []
        self.proxy_regex: str = r"\d+\.\d+\.\d+\.\d+:\d+"
        self.semaphore: asyncio.Semaphore = None

    def save_proxy(self, proxy: str) -> None:
        with open("working_proxies.txt", "a+") as proxy_file:
            proxy_file.write(proxy + "\n")

    def clear_proxy(self) -> None:
        with open("working_proxies.txt", "w+") as proxy_file:
            pass

    async def proxy_scraper(self) -> None:
        proxy_sources: List[str] = []
        with open(self.proxy_scraping_list_path, "r") as source_file:
            proxy_sources.extend(source_file.read().splitlines())

        proxy_sources = sorted(set(proxy_sources))

        async def fetch_proxy(source_link: str) -> None:
            async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(family=socket.AF_INET, ssl=False)
            ) as session:
                try:
                    async with session.get(
                        source_link,
                        headers={
                            "User-Agent": f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/{random.randint(503, 567)}.36 (KHTML, like Gecko) Chrome/{random.randint(104, 117)}.0.0.0 Safari/{random.randint(550,575)}.36"
                        },
                        timeout=self.client_timeout,
                    ) as response:
                        proxies = re.findall(self.proxy_regex, await response.text())
                        self.scraped_proxies.extend(proxies)
                except Exception as error:
                    fore.print(f"(!) Failed to process '{source_link}', Error: {error}")

        await asyncio.gather(
            *[fetch_proxy(source_link) for source_link in proxy_sources]
        )

    async def proxy_checker(self, region: Union[str, List[str]], proxy: str) -> None:
        if region == "All":
            country_check = False
        else:
            country_check = True

        ip_address = proxy.split(":")[0]
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(family=socket.AF_INET, ssl=False)
        ) as session:
            try:
                starting_time = time.monotonic()
                async with session.get(
                    self.endpoint,
                    proxy=f"http://{proxy}",
                    timeout=self.client_timeout,
                ) as response:
                    data = await response.json()
                    ending_time = time.monotonic()
                    if not country_check or data["country"] in region:
                        fore.print(
                            f"(+) Working Proxy: {proxy} | Location: {data['country']} | Speed: {abs(starting_time - ending_time):.2f}s"
                        )
                        self.save_proxy(proxy)

            except Exception:
                pass

    async def run(self, region: Union[str, List[str]], threads: int) -> None:
        await self.proxy_scraper()
        self.scraped_proxies = sorted(set(self.scraped_proxies))
        fore.print(f"[ Scraper ]  Grabbed {len(self.scraped_proxies)} proxies.")
        self.clear_proxy()

        if region == "US":
            region = self.country_list_usa
        elif region == "EU":
            region = self.country_list_eu
        elif region == "ALL":
            region = "All"
        else:
            fore.print("(!) Invalid region choice... exiting.")
            sys.exit(0)

        self.semaphore = asyncio.Semaphore(threads)

        async def check_proxy(proxy: str) -> None:
            async with self.semaphore:
                await self.proxy_checker(region, proxy)

        await asyncio.gather(*[check_proxy(proxy) for proxy in self.scraped_proxies])


async def main(region: Union[str, List[str]], threads: int) -> None:
    proxy_checker = ProxyChecker()
    await proxy_checker.run(region, threads)


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    if "nt" in os.name:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    threads = int(input("Enter the number of threads (example: 50): "))
    region = input("Enter region (example: US/EU/ALL): ").upper()
    os.system("cls" if os.name == "nt" else "clear")
    fore.print("[ Process ]  Starting ..")
    asyncio.run(main(region, threads))
      
