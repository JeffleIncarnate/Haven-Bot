import aiohttp
import urllib.request
import json
import urllib

async def get_json(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)

    return await response.json()


async def get_text(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)

    return await response.text()


def get_youtube(video_id: str) -> dict:
    params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % video_id}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        info = {
            "title": data["title"],
            "thumbnail": data["thumbnail_url"],
            "author_name": data["author_name"]
        }

        return info