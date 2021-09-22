import json
import tornado.gen
import traceback
import urllib.parse

from base64 import b64encode
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPError

from settings import Settings
from mongo_db_controller import ZoomUserDB

@tornado.gen.coroutine
def msftRefresh(msft_user):
    url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    payload = "grant_type=refresh_token&"
    payload += "client_id={0}&".format(Settings.azure_client_id)
    payload += "scope={0}&".format(urllib.parse.unquote(Settings.azure_scopes))
    payload += "refresh_token={0}&".format(msft_user.get('refresh_token'))
    payload += "redirect_uri={0}&".format(Settings.azure_redirect_uri)
    payload += "client_secret={0}".format(Settings.azure_client_secret)
    print(payload)
    headers = {
        'content-type': "application/x-www-form-urlencoded"
        }
    request = HTTPRequest(url, method="POST", headers=headers, body=payload)
    http_client = AsyncHTTPClient()
    print(msft_user)
    print('making msftRefresh')
    print(payload)
    try:
        response = yield http_client.fetch(request)
        resp = json.loads(response.body.decode("utf-8"))
        print("msftRefresh /access_token Response: {0}".format(resp))
        msft_user = ZoomUserDB.db.insert_user(msft_user['person_id'], resp['access_token'], resp['expires_in'], msft_user['refresh_token'], "msft")
        print('new msft_user:{0}'.format(msft_user))
    except HTTPError as he:
        print('msftRefresh HTTPError:')
        print(he.code)
        print(he.response.body)
        if he.code in [401, 400]:
            ZoomUserDB.db.delete_user(msft_user['person_id'], "msft")
        msft_user = None
    raise tornado.gen.Return(msft_user)

@tornado.gen.coroutine
def msftGET(url, msft_user):
    base_url = 'https://graph.microsoft.com/v1.0'
    if not url.startswith(base_url):
        url = base_url + url
    headers = {"Authorization":"Bearer {0}".format(msft_user.get('token'))}
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
            msft_user = yield msftRefresh(msft_user)
            if msft_user:
                response, msft_user = yield msftGET(url, msft_user)
        else:
            try:
                print(he.response.body)
            except Exception as e:
                pass
            traceback.print_exc()
    raise tornado.gen.Return((response, msft_user))
