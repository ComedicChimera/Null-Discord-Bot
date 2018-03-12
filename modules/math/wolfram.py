import http.client
import urllib.parse
import xml.etree.ElementTree
import PIL.Image as Image
from PIL import ImageDraw, ImageFont
import requests
from io import BytesIO


class QueryResponse:
    def __init__(self, xml_data):
        self.pods = self.extract_pods(str(xml_data))

    def extract_pods(self, xml_data):
        pods = []
        tree = xml.etree.ElementTree.fromstring(xml_data[2:-1].replace('\\n', ''))
        if tree.attrib['success']:
            for item in tree:
                if item.tag == 'pod':
                    pod = self.generate_pod(item)
                    if pod:
                        pods.append(pod)
        else:
            raise Exception(tree.attrib['error'])
        return pods

    @staticmethod
    def generate_pod(pod_obj):
        title = pod_obj.attrib['title']
        images = []
        for item in pod_obj:
            if item.tag == 'subpod':
                for elem in item:
                    if elem.tag == 'img':
                        images.append(elem.attrib)
        return Pod(title, images)


class Pod:
    def __init__(self, title, images):
        self.title = title
        self.images = images


APP_ID = 'UWXJU2-U6LRAVRT52'
DOMAIN = 'api.wolframalpha.com'
FORMAT_URL = '/v2/query?input=%s&appid=' + APP_ID


def query(query_string):
    h1 = http.client.HTTPConnection(DOMAIN)
    try:
        h1.request('GET', FORMAT_URL % urllib.parse.quote_plus(query_string))
    except:
        pass
    resp = h1.getresponse()
    return QueryResponse(resp.read())


IMAGE_X_PADDING = 10
IMAGE_Y_PADDING = 10


def add_text(img, title):
    w, h = img.size
    font = ImageFont.truetype('arial.ttf', 14)
    new_image = Image.new('RGB', (w + IMAGE_X_PADDING, h + IMAGE_Y_PADDING * 2 + 14), color=16777215)
    draw = ImageDraw.Draw(new_image)
    ts, _ = draw.textsize(title, font)
    if ts > w - IMAGE_X_PADDING:
        w = ts
    new_image = new_image.resize((w + IMAGE_X_PADDING, h + IMAGE_Y_PADDING * 2 + 14))
    draw = ImageDraw.Draw(new_image)
    draw.text((IMAGE_X_PADDING/2, IMAGE_Y_PADDING/2), title, 0, font=font)
    new_image.paste(img, (int(IMAGE_X_PADDING/2), int(IMAGE_Y_PADDING * 2 + 14)))
    return new_image


def join_images(result):
    images = []
    for item in result.pods:
        image_url = item.images[0]
        resp = requests.get(image_url['src'], stream=True)
        resp.raise_for_status()
        image = Image.open(resp.raw)
        image = add_text(image, item.title)
        images.append(image)
    h = sum([x.height for x in images])
    w = max([x.width for x in images])
    new_image = Image.new('RGB', (w, h), color=16777215)
    offset = 0
    for image in images:
        new_image.paste(image, (0, offset))
        offset += image.height
    fobj = BytesIO()
    new_image.save(fobj, format='PNG')
    return BytesIO(fobj.getvalue())


