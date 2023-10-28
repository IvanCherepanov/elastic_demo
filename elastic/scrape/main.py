import aiohttp
from bs4 import BeautifulSoup

from settings import logger


def extract_name_from_filename(url: str):
    return "-".join(url.split('/')[-2].split('-')[:-1])


def save_to_storage(html, url: str):
    # Сохраняем HTML-код в файл
    new_file_name = extract_name_from_filename(url=url)
    with open('./static/' + new_file_name + '.html', 'w', encoding='utf-8') as file:
        file.write(str(html))


async def fetch_url(url: str, timeout: int = 5):
    custom_headers = {}
    custom_data = {}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url,
                                   headers=custom_headers,
                                   data=custom_data,
                                   timeout=timeout
                                   ) as response:
                resp_bytes = await response.read()
                soup = BeautifulSoup(resp_bytes.decode(), 'html.parser')
                save_to_storage(soup, url)

                if response.status != 200:
                    return False

                return True

    except Exception as error:
        tb = error.__traceback__
        print(error.with_traceback(tb))
        logger.error(f"Error fetching {url}: {error} because {error.with_traceback(tb)}")

        return False
