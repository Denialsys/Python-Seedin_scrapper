import requests
import time
import base64
from dotenv import load_dotenv
import os
import random
import json

load_dotenv()

url = 'https://www.seedinph.tech/server/Loan/filter'
pages = 29
response_file = 'response_file.txt'

def begin_extraction(url):


    cookies = {
        '_csrf_token': os.getenv('_csrf_token'),
        '_ga': os.getenv('_ga'),
        '_gid': os.getenv('_gid'),
        'newunion_frontend': os.getenv('newunion_frontend')
    }

    form_data = {
        '_csrf_token': os.getenv('_csrf_token'),
        'product': os.getenv('product'),
        'filterType': os.getenv('filterType'),
        'page': '1'
    }
    gathered_data = ['[']

    try:
        for page in range(1, pages+1):
            form_data['page'] = str(page)
            post_response = requests.post(url, data=form_data, cookies=cookies)
            post_response = json.loads(post_response.text)
            binary_data = base64.b64decode(post_response.get('data'))

            gathered_data.append(
                json.dumps({
                    'data': json.loads(binary_data.decode('utf-8')),
                    'date': post_response.get('date')
                })
            )

            # Delay to avoid web scrapping detection
            delay = random.randrange(3, 20, 1) / 10
            print(f'Page {page} was done, delay {delay}')
            time.sleep(delay)

        gathered_data.append(']')

    except Exception as e:
        print(e.args)

    print('Writing to file')
    with open(response_file, 'w') as fileobj:
        fileobj.writelines(gathered_data)

    print('crawling was done')

if __name__ == '__main__':
    begin_extraction(url)