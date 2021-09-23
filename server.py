#!/usr/bin/env python
import os
import json
import traceback

import tornado.gen
import tornado.httpserver
import tornado.ioloop
import tornado.web

from settings import Settings
from handlers.base import BaseHandler
from handlers.oauth import AzureOAuthHandler, WebexOAuthHandler, ZoomOAuthHandler

from tornado.options import define, options, parse_command_line

define("debug", default=False, help="run in debug mode")

class MainHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        try:
            print("MainHandler GET")
            webex_user = self.get_webex_user()
            print('webex_user:{0}'.format(webex_user))
            if not webex_user:#if no webex cookie, redirect to kick off the Webex OAuth flow (starts in WebexOAuthHandler)
                self.redirect(Settings.webex_redirect_path)
            else:
                webex_user = json.loads(webex_user)
                zoom_user = self.get_zoom_user()#check for a zoom cookie
                print('zoom_user:{0}'.format(zoom_user))
                if zoom_user:
                    zoom_user = json.loads(zoom_user)
                msft_user = self.get_microsoft_user()#check for a microsoft/graph/azure cookie
                print('msft_user:{0}'.format(msft_user))
                if msft_user:
                    msft_user = json.loads(msft_user)
                #Send the cookie json objects to the main.html page, or None if they don't exist.
                self.render("main.html",
                            webex_user=webex_user,
                            zoom_user=zoom_user,
                            msft_user=msft_user,
                            zoom_oauth_path=Settings.zoom_redirect_path,
                            msft_oauth_path=Settings.azure_redirect_path)
        except Exception as e:
            traceback.print_exc()


@tornado.gen.coroutine
def main():
    try:
        parse_command_line()
        app = tornado.web.Application([
                ("/", MainHandler),
                (Settings.azure_redirect_path, AzureOAuthHandler),
                (Settings.webex_redirect_path, WebexOAuthHandler),
                (Settings.zoom_redirect_path, ZoomOAuthHandler)
              ],
            template_path=os.path.join(os.path.dirname(__file__), "html_templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret=Settings.cookie_secret,
            xsrf_cookies=False,
            debug=options.debug,
            )
        server = tornado.httpserver.HTTPServer(app)
        server.bind(Settings.port)
        print("main - Serving... on port {0}".format(Settings.port))
        server.start()
        tornado.ioloop.IOLoop.instance().start()
    except Exception as e:
        traceback.print_exc()

if __name__ == "__main__":
    main()
