import requests
from dotenv import load_dotenv
import os

load_dotenv()

url = os.environ['DATABASE_URL'] + "/data"

def load_db(url):
    try: 
        response = requests.get(url)
        data = response.json()
        return data['data']
    except:
        print('Connection failed')

db = load_db(url)