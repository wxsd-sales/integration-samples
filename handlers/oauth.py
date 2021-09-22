import json
import traceback
import urllib.parse

import tornado.gen
import tornado.web

from base64 import b64encode
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

from handlers.base import BaseHandler

from spark import Spark
from settings import Settings

class WebexOAuthHandler(BaseHandler):

    @tornado.gen.coroutine
    def get_tokens(self, code):
        url = "https://webexapis.com/v1/access_token"
        payload = "client_id={0}&".format(Settings.webex_client_id)
        payload += "client_secret={0}&".format(Settings.webex_client_secret)
        payload += "grant_type=authorization_code&"
        payload += "code={0}&".format(code)
        payload += "redirect_uri={0}".format(Settings.webex_redirect_uri)
        headers = {
            'cache-control': "no-cache",
            'content-type': "application/x-www-form-urlencoded"
            }
        try:
            request = HTTPRequest(url, method="POST", headers=headers, body=payload)
            http_client = AsyncHTTPClient()
            response = yield http_client.fetch(request)
            resp = json.loads(response.body.decode("utf-8"))
            print("WebexOAuthHandler.get_tokens /access_token Response: {0}".format(resp))
            person = yield Spark(resp["access_token"]).get_with_retries_v2('https://api.ciscospark.com/v1/people/me')
            person.body.update({"token":resp["access_token"]})
            print(person.body)
            self.set_secure_cookie("Webex-User", json.dumps(person.body), expires_days=1, version=2)
        except Exception as e:
            print("WebexOAuthHandler.get_tokens Exception:{0}".format(e))
            traceback.print_exc()



    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        response = "Error"
        try:
            print('Webex OAuth: {0}'.format(self.request.full_url()))
            if not self.get_webex_user():
                if self.get_argument("code", None):
                    code = self.get_argument("code")
                    yield self.get_tokens(code)
                    self.redirect("/")
                    return
                else:
                    authorize_url = 'https://webexapis.com/v1/authorize?client_id={0}&response_type=code&redirect_uri={1}&scope={2}'
                    authorize_url = authorize_url.format(Settings.webex_client_id, urllib.parse.quote_plus(Settings.webex_redirect_uri), Settings.webex_scopes)
                    print("WebexOAuthHandler.get authorize_url:{0}".format(authorize_url))
                    self.redirect(authorize_url)
                    return
            else:
                print("Already authenticated.")
                self.redirect("/")
                return
        except Exception as e:
            response = "{0}".format(e)
            print("WebexOAuthHandler.get Exception:{0}".format(e))
            traceback.print_exc()
        self.write(response)


class ZoomOAuthHandler(BaseHandler):

    @tornado.gen.coroutine
    def get_tokens(self, code):
        url = "https://zoom.us/oauth/token"
        payload = "grant_type=authorization_code&"
        payload += "code={0}&".format(code)
        payload += "redirect_uri={0}".format(Settings.zoom_redirect_uri)

        #we need to base 64 encode it
        #and then decode it to acsii as python 3 stores it as a byte string
        userAndPass = b64encode("{0}:{1}".format(Settings.zoom_client_id, Settings.zoom_client_secret).encode()).decode("ascii")
        print(userAndPass)
        print(type(userAndPass))

        headers = {
            'authorization': 'Basic {0}'.format(userAndPass),
            'cache-control': "no-cache",
            'content-type': "application/x-www-form-urlencoded"
            }
        try:
            request = HTTPRequest(url, method="POST", headers=headers, body=payload)
            http_client = AsyncHTTPClient()
            response = yield http_client.fetch(request)
            resp = response.body.decode("utf-8")
            print("ZoomOAuthHandler.get_tokens /access_token Response: {0}".format(resp))
            self.set_secure_cookie("Zoom-User", resp, expires_days=1, version=2)
        except Exception as e:
            print("ZoomOAuthHandler.get_tokens Exception:{0}".format(e))
            traceback.print_exc()



    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        response = "Error"
        try:
            print('Zoom OAuth: {0}'.format(self.request.full_url()))
            webex_user = self.get_webex_user()
            print(webex_user)
            if webex_user:
                if not self.get_zoom_user():
                    if self.get_argument("code", None):
                        code = self.get_argument("code")
                        yield self.get_tokens(code)
                        self.redirect("/")
                        return
                    else:
                        authorize_url = 'https://zoom.us/oauth/authorize?response_type=code&client_id={0}&redirect_uri={1}'.format(Settings.zoom_client_id, urllib.parse.quote_plus(Settings.zoom_redirect_uri))
                        print("ZoomOAuthHandler.get authorize_url:{0}".format(authorize_url))
                        self.redirect(authorize_url)
                        return
                else:
                    print("Already Zoom Authenticated.")
                    self.redirect("/")
                    return
            else:
                print("No Webex authentication.")
                self.redirect("/")
                return
        except Exception as e:
            response = "{0}".format(e)
            print("ZoomOAuthHandler.get Exception:{0}".format(e))
            traceback.print_exc()
        self.write(response)


class AzureOAuthHandler(BaseHandler):

    @tornado.gen.coroutine
    def get_tokens(self, code):
        url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
        payload = "grant_type=authorization_code&"
        payload += "client_id={0}&".format(Settings.azure_client_id)
        payload += "scope={0}&".format(urllib.parse.unquote(Settings.azure_scopes))
        payload += "code={0}&".format(code)
        payload += "redirect_uri={0}&".format(Settings.azure_redirect_uri)
        payload += "client_secret={0}".format(Settings.azure_client_secret)
        print(payload)
        headers = {
            'content-type': "application/x-www-form-urlencoded"
            }
        try:
            request = HTTPRequest(url, method="POST", headers=headers, body=payload)
            http_client = AsyncHTTPClient()
            response = yield http_client.fetch(request)
            resp = response.body.decode("utf-8")
            print("AzureOAuthHandler.get_tokens /access_token Response: {0}".format(resp))
            self.set_secure_cookie("Msft-User", resp, expires_days=1, version=2)
        except Exception as e:
            print("AzureOAuthHandler.get_tokens Exception:{0}".format(e))
            traceback.print_exc()



    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        response = "Error"
        try:
            print(self.request)
            print(dir(self.request))
            print('Azure OAuth: {0}'.format(self.request.full_url()))
            webex_user = self.get_webex_user()
            print(webex_user)
            if webex_user:
                if not self.get_microsoft_user():
                    if self.get_argument("code", None):
                        code = self.get_argument("code")
                        yield self.get_tokens(code)
                        self.redirect("/")
                        return
                    else:
                        authorize_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={0}&response_type=code'.format(Settings.azure_client_id)
                        authorize_url += '&redirect_uri={0}&response_mode=query&scope=offline_access%20{1}&state=12345'.format(urllib.parse.quote_plus(Settings.azure_redirect_uri), Settings.azure_scopes)
                        print("AzureOAuthHandler.get authorize_url:{0}".format(authorize_url))
                        self.redirect(authorize_url)
                        return
                else:
                    print("Already Azure Authenticated.")
                    self.redirect("/")
                    return
            else:
                print("No Azure authentication.")
                self.redirect("/")
                return
        except Exception as e:
            response = "{0}".format(e)
            print("AzureOAuthHandler.get Exception:{0}".format(e))
            traceback.print_exc()
        self.write(response)
