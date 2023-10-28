from typing import List
from bs4 import BeautifulSoup
from settings import logger
from elastic.schema import Quote


def parse_panda_page_for_quotes(soup: BeautifulSoup) -> List[Quote]:
    answer_list: List[Quote] = []

    quotes_block = soup.find("div", class_='open-list-items clearfix')
    if not quotes_block:
        return []

    quote_block_elements = quotes_block.find_all("div", class_='open-list-item open-list-block clearfix')
    logger.info(f"quote_block_elements: {len(quote_block_elements)}")

    for quote_block_element in quote_block_elements:
        paragraph = quote_block_element.find("p", class_='post-content-description')
        paragraph_div = quote_block_element.find('div', class_='bordered-description')

        if paragraph:
            data_quote = paragraph.find('span', class_='bordered-description')
        elif paragraph_div:
            data_quote = paragraph_div.find('p')
        else:
            continue

        if data_quote:
            quote_text = data_quote.text

            if "-" in quote_text:
                split_data = quote_text.split("-")
            elif "—" in quote_text:
                split_data = quote_text.split("—")
            elif "–" in quote_text:
                split_data = quote_text.split("–")
            else:
                logger.warning(f"processing later {quote_text}")
                continue

            character = split_data[-1]
            text = "".join(split_data[:-1])
            quote_object = Quote(
                character=character,
                text=text
            )
            answer_list.append(quote_object)

    return answer_list
