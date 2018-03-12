import requests
import PIL.Image as Image
from io import BytesIO


LATEX_URL = 'http://rtex.probablyaweb.site/api/v2'


def generate(code):
    code = open('modules/math/templates/template.tex').read().replace('#USERCODE', code)
    return download_image(LATEX_URL + '/' + get_file_path(code))


def get_file_path(code):
    payload = {
        'code': code,
        'format': 'png'
    }
    resp = requests.post(LATEX_URL, data=payload)
    resp.raise_for_status()
    jdata = resp.json()
    if jdata['status'] != 'success':
        if 'log' in jdata:
            log = jdata['log']
            ndx = log.find('LaTeX Error')
            log = log[ndx:]
            ndx = log.find('\n')
            raise Exception(log[:ndx])
        else:
            raise Exception('LaTex Error')
    return jdata['filename']


def download_image(url):
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    image = Image.open(resp.raw).convert('RGBA')
    new_image = Image.new('RGBA', (image.width + 10, image.height + 10), color=(255, 255, 255, 255))
    new_image.paste(image, mask=image.split()[-1], box=(5, 5))
    fobj = BytesIO()
    new_image.save(fobj, format='PNG', quality=95)
    return BytesIO(fobj.getvalue())


def generate_eqn(code):
    code = open('modules/math/templates/equation.tex').read().replace('#USERCODE', code)
    return download_image(LATEX_URL + '/' + get_file_path(code))