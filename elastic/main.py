from typing import Union


from bs4 import BeautifulSoup
from elastic.parse.main import parse_panda_page_for_quotes
from elastic.inject import client_elastic


def check_exist_index(index_value: str):
    return client_elastic.indices.exists(index_value)


def create_custom_index(index_value: str):
    created = False
    try:
        if not check_exist_index(index_value):
            # Ignore 400 means to ignore "Index Already Exist" error.
            client_elastic.indices.create(index=index_value, ignore=400)
            print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created


def create_document(index_name: str, document_data: dict):
    client_elastic.index(
        index=index_name, body=document_data
    )


def use_search(index_name: Union[None, str], search_dict: dict):
    query = {
        "size": 100,
        "query": {
            "match": search_dict
        }
    }
    return client_elastic.search(index=index_name, body=query)


def start_load():
    create_custom_index("lord-of-the-rings")

    with open('static/example.html', 'r',
              encoding='utf-8') as html_file:
        data = html_file.read()

    result = parse_panda_page_for_quotes(soup=BeautifulSoup(data, features="lxml"))
    print(len(result))
    for item in result:
        create_document(index_name="lord-of-the-rings", document_data=item.dict())


def create_index_load_data_from_page(soup: BeautifulSoup, index_name: str):
    create_custom_index(index_value=index_name)
    result = parse_panda_page_for_quotes(soup=soup)
    print(len(result))
    for item in result:
        create_document(index_name=index_name, document_data=item.dict())