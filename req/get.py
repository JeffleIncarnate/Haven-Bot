import aiohttp


async def get_json(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)

    return await response.json()


async def get_text(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)

    return await response.text()
