from pprint import pprint

from bs4 import BeautifulSoup
from fastapi import FastAPI, UploadFile, File, Form
import uvicorn
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from settings import logger, config
from elastic.main import create_index_load_data_from_page, use_search, check_exist_index, start_load
from elastic.schema import SearchRequest, SearchUrl
from elastic.scrape.main import fetch_url, extract_name_from_filename

app = FastAPI()


# @app.on_event("startup")
# async def startup_event():
#     if not check_exist_index(index_value='lord-of-the-rings'):
#         start_load()


@app.get("/")
def read_root():
    logger.info(f"called")
    return {"Hello": "world"}


# Подключаем статическую папку для хранения загруженных HTML-документов
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post("/upload_html/",
          description="Upload html-page with quotes from source")
async def upload_html(file: UploadFile = File(...), filename: str = Form(...)):
    try:
        # Читаем содержимое HTML-файла
        html_content = await file.read()

        # Записываем содержимое в статическую папку с указанным именем файла
        with open(f"static/{filename}.html", "wb") as file:
            file.write(html_content)

        with open(f"static/{filename}.html", 'r', encoding='utf-8') as html_file:
            data = html_file.read()

        create_index_load_data_from_page(soup=BeautifulSoup(data, features="lxml"),
                                         index_name=filename)

        return JSONResponse(status_code=200, content="data loaded")
    except Exception as e:
        logger.error(f"{str(e)} and {e.with_traceback(e.__traceback__)}")
        return JSONResponse(status_code=500, content=str(e))


@app.post("/search/",
          description=f"Search by key:value parameter text-data or character-data & index name")
async def search(search_request: SearchRequest):
    try:
        result = use_search(search_request.index_name, search_request.search_dict)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)})


@app.post("/load_url/",
          description="Load data from url")
async def search(search_request: SearchUrl):
    try:
        result = await fetch_url(url=search_request.url)
        if result:
            filename = extract_name_from_filename(url=search_request.url)

            with open(f"static/{filename}.html", 'r', encoding='utf-8') as html_file:
                data = html_file.read()

            create_index_load_data_from_page(soup=BeautifulSoup(data, features="lxml"),
                                             index_name=filename)

            return JSONResponse(status_code=200, content="data loaded")

        return JSONResponse(status_code=400, content=f"Problem with fetch data")
    except Exception as e:
        logger.error(f"{str(e)} and {e.with_traceback(e.__traceback__)}")
        JSONResponse(status_code=500, content=str(e))


if __name__ == "__main__":
    if not check_exist_index(index_value='lord-of-the-rings'):
        start_load()
    uvicorn.run(app, host="0.0.0.0", port=config.app_port)
