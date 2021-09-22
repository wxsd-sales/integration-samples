import os
from dotenv import load_dotenv
from urllib.parse import urljoin

load_dotenv()

class Settings(object):
	port = int(os.environ.get("MY_APP_PORT"))
	base_url = os.environ.get("MY_BASE_URL")
	cookie_secret = os.environ.get("UNIQUE_COOKIE_SECRET")

	webex_client_id = os.environ.get("MY_WEBEX_CLIENT_ID")
	webex_client_secret = os.environ.get("MY_WEBEX_SECRET")
	webex_redirect_path = os.environ.get("MY_WEBEX_REDIRECT_PATH")
	webex_redirect_uri = urljoin(base_url, webex_redirect_path)
	webex_scopes = os.environ.get("MY_WEBEX_SCOPES")

	zoom_client_id = os.environ.get("MY_ZOOM_CLIENT_ID")
	zoom_client_secret = os.environ.get("MY_ZOOM_SECRET")
	zoom_redirect_path = os.environ.get("MY_ZOOM_REDIRECT_PATH")
	zoom_redirect_uri = urljoin(base_url, zoom_redirect_path)

	azure_client_id = os.environ.get("MY_AZURE_CLIENT_ID")
	azure_client_secret = os.environ.get("MY_AZURE_SECRET")
	azure_redirect_path = os.environ.get("MY_AZURE_REDIRECT_PATH")
	azure_redirect_uri = urljoin(base_url, azure_redirect_path)
	azure_scopes = os.environ.get("MY_AZURE_SCOPES")
