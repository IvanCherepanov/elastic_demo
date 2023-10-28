import time

from elasticsearch import Elasticsearch

from settings import logger, config
import subprocess


def connect_elasticsearch():
    _es = None

    while True:
        try:
            result = subprocess.run(
                ["curl", "-s", "http://" + config.elasticsearch_server + ":" + str(config.elasticsearch_port_int)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            if result.returncode == 0:
                logger.debug("Elasticsearch доступен")
                print("Elasticsearch доступен")
                break
            else:
                logger.debug("Elasticsearch недоступен - ждем...")
                print("Elasticsearch недоступен - ждем...")
                time.sleep(10)
        except Exception as e:
            # Обработка исключений при возникновении ошибок
            print(f"Ошибка: {e}")
            time.sleep(10)

    try:
        # subprocess.run(["curl", "http://elasticsearch_cont:9200"])
        # subprocess.run(["curl", "http://127.0.0.1:9200"])
        # subprocess.run(["curl", "http://elasticsearch_cont:9200/random-movie/_search"])

        _es = Elasticsearch(
            [
                {'host': config.elasticsearch_server,
                 'port': config.elasticsearch_port_int,
                 'scheme': "http"
                 }
            ]
        )
        if _es.ping():
            print('Yay Connected')
        else:
            print('Awww it could not connect!')
        return _es

    except Exception as e:
        logger.warning(f"{e.with_traceback(e.__traceback__)}")


client_elastic = connect_elasticsearch()
