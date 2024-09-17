"""
Ad-hoc script to build the car database tables with iRacing & Garage61 car data.

Set
- IRACING_EMAIL
- IRACING_PW
- GARAGE61_TOKEN

in your environment variables before running this script.

Run using `python3 build_car_list.py`
"""

import requests
import hashlib
import base64
import json
import os
import duckdb
import numpy, pandas

## General Functions
def login_to_iracing() -> requests.Session:
    session = requests.Session()
    
    def encode_pw(username: str, password: str):
        initialHash = hashlib.sha256((password + username.lower()).encode('utf-8')).digest()
        hashInBase64 = base64.b64encode(initialHash).decode('utf-8')
        return hashInBase64
    
    body = {
        'email': os.environ.get('IRACING_EMAIL'),
        'password': encode_pw(os.environ.get('IRACING_EMAIL'), os.environ.get('IRACING_PW'))
    }
    
    response = session.post(url='https://members-ng.iracing.com/auth', json=body)
    
    if response.status_code != 200:
        raise Exception(f'Failed to login to iRacing: {response.status_code}')
    else:
        return session
    
def login_to_speedweek():
    session = requests.Session()
    # ask the user for their email and password
    username = os.environ.get('SPEEDWEEK_EMAIL')
    password = os.environ.get('SPEEDWEEK_PW')
    body = {
        'username': username,
        'password': password
    }
    response = session.post('http://localhost:8000/auth/jwt/login', data=body)
    
    if response.status_code != 200:
        raise Exception(f'Failed to login to Speedweek: {response.status_code}')
    
    access_token = response.json()['access_token']
    return access_token
    
#### Car Data
def get_iracing_cars(session: requests.Session) -> dict:
    response = session.get(url='https://members-ng.iracing.com/data/car/get')
    res_json = response.json()
    url = res_json['link']
    car_data = session.get(url)
    
    if not os.path.exists('temp'):
        os.mkdir('temp')
        
    with open('temp/cars.json', 'wb') as f:
        f.write(car_data.content)
    return res_json

def get_iracing_car_assets(session: requests.Session) -> dict:
    response = session.get(url='https://members-ng.iracing.com/data/car/assets')
    res_json = response.json()
    url = res_json['link']
    car_data = session.get(url)
    
    if not os.path.exists('temp'):
        os.mkdir('temp')
    
    cars_json = car_data.json()
    cars_list = list(cars_json.values())
    json_array = json.dumps(cars_list, indent=4)
        
    with open('temp/car_assets.json', 'w') as f:
        f.write(json_array)
    return res_json

def get_garage61_cars():
    header = {
        'Authorization': f'Bearer {os.environ.get("GARAGE61_TOKEN")}'
    }
    response = requests.get(url='https://garage61.net/api/v1/cars', headers=header)
    if response.status_code != 200:
        raise Exception(f'Failed to get cars from Garage61: {response.status_code}')
    
    items = response.json()['items']
    
    with open('temp/garage61_cars.json', 'w') as f:
        f.write(json.dumps(items))
    return response.json()

def get_speedweek_cars(access_token):

    headers = {'Authorization': f'Bearer {access_token}'}
    
    my_cars = requests.get('http://localhost:8000/cars', headers=headers)
    
    with open('temp/my_cars.json', 'w') as f:
        f.write(json.dumps(my_cars.json()['data'], indent=4))
    
    
def build_car_list():
    sql = """
    SELECT *
    FROM (
        SELECT
            car_name,
            car.car_id as iracing_car_id,
            array_extract(categories, 1) AS car_category,
            'https://images-static.iracing.com' || asset.folder || '/' || asset.small_image AS iracing_car_picture,
            garage61.id as garage61_car_id,
        FROM read_json_auto('temp/cars.json') car

        LEFT JOIN read_json_auto('temp/car_assets.json') asset
        ON car.car_id = asset.car_id

        LEFT JOIN read_json_auto('temp/garage61_cars.json') garage61
        on car.car_id = garage61.platform_id
    )

    """
    #    
    #--EXCEPT
    #--
    #--SELECT car_name, iracing_car_id, car_category, iracing_car_picture, garage61_car_id
    #--FROM read_json_auto('temp/my_cars.json')
    #--
    # --LIMIT 10
    
    db = duckdb.connect()
    db.execute(sql)
    car_items = db.fetch_df()
    return car_items

def apply_car_to_speedweek(row, access_token):
    body = {
        'car_name': row.car_name,
        'car_category': row.car_category,
        'iracing_car_id': row.iracing_car_id,
        'iracing_car_picture': row.iracing_car_picture,
        'garage61_car_id': row.garage61_car_id
    }
    header = {'Authorization': f'Bearer {access_token}'}
    response = requests.post('http://localhost:8000/cars', json=body, headers=header)
    if response.status_code != 200:
        print(f'Failed to create car {row.car_name}: {response.status_code}')
        print(response.json())
        print(body)
        print('-------------------')
        
        
# Tracks

def get_iracing_tracks(session: requests.Session) -> dict:
    response = session.get(url='https://members-ng.iracing.com/data/track/get')
    res_json = response.json()
    url = res_json['link']
    track_data = session.get(url)
    
    if not os.path.exists('temp'):
        os.mkdir('temp')
        
    with open('temp/tracks.json', 'wb') as f:
        f.write(track_data.content)
    return res_json

def get_iracing_track_assets(session: requests.Session) -> dict:
    response = session.get(url='https://members-ng.iracing.com/data/track/assets')
    res_json = response.json()
    url = res_json['link']
    track_data = session.get(url)
    
    if not os.path.exists('temp'):
        os.mkdir('temp')
    
    tracks_json = track_data.json()
    tracks_list = list(tracks_json.values())
    json_array = json.dumps(tracks_list, indent=4)
        
    with open('temp/track_assets.json', 'w') as f:
        f.write(json_array)
    return res_json

def get_garage61_tracks():
    header = {
        'Authorization': f'Bearer {os.environ.get("GARAGE61_TOKEN")}'
    }
    response = requests.get(url='https://garage61.net/api/v1/tracks', headers=header)
    if response.status_code != 200:
        raise Exception(f'Failed to get tracks from Garage61: {response.status_code}')
    
    items = response.json()['items']
    
    with open('temp/garage61_tracks.json', 'w') as f:
        f.write(json.dumps(items))
        
    return response.json()

def build_track_list():
    sql = """
    SELECT *
    FROM (
        SELECT
            track.track_name,
            track.config_name as config,
            track.track_id as iracing_id,
            'https://images-static.iracing.com' || asset.folder || '/' || asset.small_image AS iracing_image_url,
            garage61.id as garage61_id,
        FROM read_json_auto('temp/tracks.json') track

        LEFT JOIN read_json_auto('temp/track_assets.json') asset
        ON track.track_id = asset.track_id

        LEFT JOIN read_json_auto('temp/garage61_tracks.json') garage61
        on track.track_id = garage61.platform_id
    )
    """
    db = duckdb.connect()
    db.execute(sql)
    track_items = db.fetch_df()
    return track_items

def apply_track_to_speedweek(row, access_token):
    body = {
        'name': row.track_name,
        #'config': row.config,
        'iracing_id': row.iracing_id,
        'iracing_image_url': row.iracing_image_url,
        'garage61_id': row.garage61_id
    }
    if not pandas.isnull(row.config):
        body['config'] = row.config
    
    header = {'Authorization': f'Bearer {access_token}'}
    response = requests.post('http://localhost:8000/tracks', json=body, headers=header)
    if response.status_code != 200:
        print(f'Failed to create track {row.name}: {response.status_code}')
        print(response.json())
    
    
def clean_up():
    os.remove('temp/cars.json')
    os.remove('temp/car_assets.json')
    os.remove('temp/garage61_cars.json')
    os.rmdir('temp')


iracing_session = login_to_iracing()
speedweek_access_token = login_to_speedweek()

#iracing_cars = get_iracing_cars(iracing_session)
#iracing_car_assets = get_iracing_car_assets(iracing_session)
#garage61_cars = get_garage61_cars()
#get_speedweek_cars(speedweek_access_token)
car_list = build_car_list()
car_list.apply(apply_car_to_speedweek, axis=1, args=(speedweek_access_token,))


#tracks = get_iracing_tracks(iracing_session)
#track_assets = get_iracing_track_assets(iracing_session)
#garage61_tracks = get_garage61_tracks()
track_df = build_track_list()
track_df.apply(apply_track_to_speedweek, axis=1, args=(speedweek_access_token,))

# clean_up()


