import aiohttp
import asyncio
import math

HEADERS = {'user-agent': """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"""}

async def get_hackathons_page(page: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://devpost.com/api/hackathons?page={page}', headers = HEADERS) as response:
            try: return await response.json()
            except Exception: return page

async def get_all_hackathons_pages():
    hackathons = []
    first = await get_hackathons_page(1)
    total_pages = math.ceil(first['meta']['total_count'] / first['meta']['per_page'])
    all = await get_pages_hackathons([page for page in range(1, total_pages + 1)])
    failed = [page for page in all if type(page) == int]
    hackathons = [hackathon for hackathons in all  if type(hackathons) == dict for hackathon in hackathons['hackathons']]
    while True:
        fetched = await get_pages_hackathons(failed)
        failed = [page for page in fetched if type(page) == int]
        hackathons.extend([hackathon for hackathons in fetched if type(hackathons) == dict for hackathon in hackathons['hackathons']])
        if not failed: break   
    return hackathons

async def get_pages_hackathons(pages: list):
    return await asyncio.gather(*[get_hackathons_page(page) for page in pages])
