from flask import Flask, render_template
import requests
from datetime import datetime

"""Autor

Edgar Omar Najera Vazquez
"""

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY = 'dev',
    DEBUG = False
)

URL = 'https://epic.gsfc.nasa.gov/api/natural'

def get_url(date:str,image:str) -> list:
    fecha = datetime.strptime(date, r'%Y-%m-%d %H:%M:%S')
    image_url = 'https://epic.gsfc.nasa.gov/archive/natural/{}/{}/{}/png/{}.png'.format(fecha.year,fecha.month,fecha.day,image)
    return image_url

def crear_datos(datos:dict) -> dict:
    data = {}
    count = 0
    for elemento in datos:
        data[count] = {
            'caption': elemento['caption'],
            'image_name': elemento['image'],
            'image_url': get_url(elemento['date'], elemento['image']),
            'date': elemento['date'],
            'version': elemento['version']
        }
        count += 1
    return data


@app.route('/')
def index():
    data = requests.get(URL)
    data = data.json()
    data = crear_datos(data)
    return render_template('index.html', data=data)