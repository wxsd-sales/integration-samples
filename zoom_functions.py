import json
import tornado.gen
import traceback

from base64 import b64encode
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPError

from settings import Settings
from mongo_db_controller import ZoomUserDB

@tornado.gen.coroutine
def zoomRefresh(zoom_user):
    url = "https://zoom.us/oauth/token"
    payload = "grant_type=refresh_token&"
    payload += "refresh_token={0}".format(zoom_user.get('refresh_token'))
    #we need to base 64 encode it
    #and then decode it to acsii as python 3 stores it as a byte string
    userAndPass = b64encode("{0}:{1}".format(Settings.zoom_client_id, Settings.zoom_client_secret).encode()).decode("ascii")
    headers = {
        'authorization': 'Basic {0}'.format(userAndPass),
        'content-type': "application/x-www-form-urlencoded"
        }
    request = HTTPRequest(url, method="POST", headers=headers, body=payload)
    http_client = AsyncHTTPClient()
    print(zoom_user)
    print('making zoomRefresh')
    print(payload)
    try:
        response = yield http_client.fetch(request)
        resp = json.loads(response.body.decode("utf-8"))
        print("zoomRefresh /access_token Response: {0}".format(resp))
        zoom_user = ZoomUserDB.db.insert_user(zoom_user['person_id'], resp['access_token'], resp['expires_in'], resp['refresh_token'], "zoom")
        print('new zoom_user:{0}'.format(zoom_user))
    except HTTPError as he:
        print('zoomRefresh HTTPError:')
        print(he.code)
        print(he.response.body)
        if he.code == 401:
            ZoomUserDB.db.delete_user(zoom_user['person_id'], "zoom")
        zoom_user = None
    raise tornado.gen.Return(zoom_user)

@tornado.gen.coroutine
def zoomGET(endpoint_url, zoom_user):
    url = "https://api.zoom.us/v2{0}".format(endpoint_url)
    headers = {"Authorization":"Bearer {0}".format(zoom_user.get('token'))}
    request = HTTPRequest(url, method="GET", headers=headers)
    http_client = AsyncHTTPClient()
    response = None
    try:
        response = yield http_client.fetch(request)
        body = response.body.decode('utf-8')
        response = json.loads(body)
    except HTTPError as he:
        if he.code == 401:
            print('token may be expired, attempting refresh')
            zoom_user = yield zoomRefresh(zoom_user)
            if zoom_user:
                response, zoom_user = yield zoomGET(endpoint_url, zoom_user)
        else:
            try:
                print(he.response.body)
            except Exception as e:
                pass
            traceback.print_exc()
    raise tornado.gen.Return((response, zoom_user))
