import json
import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def get_webex_user(self):
        cookie = self.get_secure_cookie("Webex-User", max_age_days=1, min_version=2)
        return cookie

    def get_zoom_user(self):
        cookie = self.get_secure_cookie("Zoom-User", max_age_days=1, min_version=2)
        return cookie

    def get_microsoft_user(self):
        cookie = self.get_secure_cookie("Msft-User", max_age_days=1, min_version=2)
        return cookie
