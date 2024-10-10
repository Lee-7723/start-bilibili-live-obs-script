import obspython, json, requests

room_id = ''
area_id: int = 610
cookie: str = ''
# csrf: str = ''

def startLive(csrf: str, area_id: int, room_id: int|str, cookie: str) -> dict:
    resp = requests.post(
        "https://api.live.bilibili.com/room/v1/Room/startLive",
        data={
            "room_id": room_id,
            "platform": "pc",
            "area_v2": area_id,
            "backup_stream": 0,
            "csrf_token": csrf,
            "csrf": csrf,
        },
        headers={
            "User-Agent": "hahaha",
            "Cookie": cookie,
        },
    )
    resp_d = resp.json()
    if resp_d['code'] != 0:
        raise Exception(f'error when post request to startLive \n {resp.content.decode()}')
    print(resp.content.decode())
    return resp.json()

def stopLive(csrf: str, room_id: int|str, cookie: str) -> dict:
    resp = requests.post(
        "https://api.live.bilibili.com/room/v1/Room/stopLive",
        data={
            "room_id": room_id,
            "platform": "pc",
            "csrf_token": csrf,
            "csrf": csrf,
        },
        headers={
            "User-Agent": "hahaha",
            "Cookie": cookie,
        },
    )
    resp_d = resp.json()
    if resp_d['code'] != 0:
        raise Exception(f'error when post request to startLive \n {resp.content.decode()}')
    print(resp.content.decode())
    return resp.json()

def set_service(server: str, key: str):
    settings: dict = {'server': server, 'key': key}
    settings: str = json.dumps(settings)
    settings = obspython.obs_data_create_from_json(settings)

    service = obspython.obs_service_create('rtmp_custom', 'rtmp', settings, None)
    obspython.obs_frontend_set_streaming_service(service)

    obspython.obs_service_release(service)
    obspython.obs_data_release(settings)

def handle_start(props, prop):
    'cookie string must contain "SESSDATA" and "bili_jct"'
    global cookie, room_id, area_id

    for item in cookie.replace(' ', '').split(';'):
        key, value = item.split('=')
        if key == 'bili_jct':
            csrf = value

    start_info = startLive(csrf, area_id, room_id, cookie)
    addr: str = start_info['data']['rtmp']['addr']
    code: str = start_info['data']['rtmp']['code']
    set_service(server=addr, key=code)
    obspython.obs_frontend_streaming_start()
    
def handle_stop(props, prop):
    global cookie, room_id, area_id

    for item in cookie.replace(' ', '').split(';'):
        key, value = item.split('=')
        if key == 'bili_jct':
            csrf = value

    stopLive(csrf, room_id, cookie)
    obspython.obs_frontend_streaming_stop()

    
def script_description():
    return 'start bilibili live from web api'


def script_update(settings):
    global cookie, room_id, area_id
    cookie = obspython.obs_data_get_string(settings, 'cookie')
    area_id = obspython.obs_data_get_int(settings, 'area_id')
    room_id = obspython.obs_data_get_string(settings, 'room_id')
    obspython.obs_data_save_json(settings, script_path() + 'config.json')

def script_properties():
    props = obspython.obs_properties_create()
    obspython.obs_properties_add_text(props, "room_id", "room id", obspython.OBS_TEXT_DEFAULT)
    obspython.obs_properties_add_int(props, "area_id", "area id", 0, 1000, 1)
    obspython.obs_properties_add_text(props, "cookie", "cookie", obspython.OBS_TEXT_DEFAULT)
    # obspython.obs_properties_add_text(props, "csrf", "csrf", obspython.OBS_TEXT_DEFAULT)

    obspython.obs_properties_add_button(props, 'start_live', 'start live && pushing', handle_start)
    obspython.obs_properties_add_button(props, 'stop_live', 'stop live && pushing', handle_stop)
    # obspython.obs_properties_add_button(props, 'set_service', 'set service', handle_set_service)

    return props
