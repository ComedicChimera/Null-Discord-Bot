import requests
from bs4 import BeautifulSoup
import urllib.parse


JOKE_URL = 'https://icanhazdadjoke.com'
URBAN_URL = 'http://api.urbandictionary.com/v0/define?term=%s'
IMG_FLIP_URL = 'https://api.imgflip.com/caption_image'


def get_joke():
    resp = requests.get(JOKE_URL)
    resp.raise_for_status()
    data = resp.text
    soup = BeautifulSoup(data, 'html.parser')
    res = soup.findAll('div', {'class': 'card-content'})[0].findAll('p', {'class': 'subtitle'})[0].contents[0]
    return res


def get_urban_definition(query):
    resp = requests.get(URBAN_URL % urllib.parse.quote_plus(query))
    resp.raise_for_status()
    jdata = resp.json()
    if jdata['result_type'] == 'exact':
        return jdata['list'][0]
    else:
        raise Exception('Result not exact.')

templates = {
    'onedoesnotsimply': 61579,
    'batman': 438680,
    'mostinteresting': 61532,
    'thatwouldbegreat': 563423,
    'facepalm': 1509839,
    'nutbutton': 119139145,
    'anditsgone': 766986,
    'twobuttons': 87743020,
    'steveharvey': 143601,
    'futuramafry': 61520
}

IMG_FLIP_USERNAME = 'ComedicChimera'

# unique and random password, unimportant, no security protection necessary
IMG_FLIP_PASSWORD = 'memelord48'


def get_custom_meme(template_alias, top_text=' ', bottom_text=' '):
    payload = {
        'template_id': templates[template_alias],
        'text0': top_text,
        'text1': bottom_text,
        'username': IMG_FLIP_USERNAME,
        'password': IMG_FLIP_PASSWORD
    }
    resp = requests.post(IMG_FLIP_URL, data=payload)
    resp.raise_for_status()
    jdata = resp.json()
    if not jdata['success']:
        raise Exception(jdata['error_message'])
    image_url = jdata['data']['url']
    img_resp = requests.get(image_url, stream=True)
    img_resp.raise_for_status()
    return img_resp.raw


def get_cat_fact():
    resp = requests.get('https://catfact.ninja/fact')
    resp.raise_for_status()
    return resp.json()['fact']
