import json
import logging
import os
import requests

import azure.functions as func

def main(everyDayAt5AM: func.TimerRequest, products: func.SqlRowList) -> None:
    logging.info('Python timer trigger function started')
    # convert the SQL data to JSON in memory
    rows = list(map(lambda r: json.loads(r.to_json()), products))

    # get the API endpoint from app settings
    api_url = os.environ['API_URL']

    # send the data to the API
    response = requests.post(api_url, json=rows)
    # check for 2xx status code
    if response.status_code // 100 != 2:
        logging.error(f"API response: {response.status_code} {response.reason}")
    else:
        logging.info(f"API response: {response.status_code} {response.reason}")