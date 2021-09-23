<p align="center">
  <h2 align="center"> Integration Samples</h2>

  <p align="center">
    This demo can be used to Authenticate through OAuth to Webex, Zoom and Microsoft Azure.  It is intended to help developers understand the OAuth Authorization grant process flow.
    <br />
    <a href="https://integration-samples.wbx.ninja/"><strong>View Demo</strong></a>
    ·
    <a href="https://github.com/WXSD-Sales/integration-samples/issues"><strong>Report Bug</strong></a>
    ·
    <a href="https://github.com/WXSD-Sales/integration-samples/issues"><strong>Request Feature</strong></a>
  </p>
</p>

## About The Project

Video Walkthrough Coming Soon.


### Flow Diagram

![image](https://user-images.githubusercontent.com/19175490/134587510-c5d7285a-abe5-4974-806c-c72846b4818f.png)
Image courtesy of [Auth0](https://auth0.com/docs/authorization/flows/authorization-code-flow)

<!-- GETTING STARTED -->

### Built With

python v3.7.4

### Installation

1. Clone this repo, then make sure you have the folowing python packages installed (may need to use pip3, depending on your python installation)
   ```sh
    pip install python-dotenv
    pip install tornado==4.5.2
    pip install requests
    pip install requests-toolbelt
   ```
2. You will need to create a file in the root directory call **.env** (you can copy or rename the **sample.env** file to **.env**)
   Then, see the section below titled "Environment Variables"
3. Start the server (use --debug to listen for changes in the python code)
   ```sh
   python server.py --debug
   ```
   
### Environment Variables

The following Environment Variables are required.  You can fill them out using the sample.env file, then rename the file to .env
```
MY_APP_PORT=8000
MY_BASE_URL=https://1234.eu.ngrok.io/
UNIQUE_COOKIE_SECRET=CHANGETHISTOUNIQUEVALUE

MY_WEBEX_CLIENT_ID=
MY_WEBEX_SECRET=
MY_WEBEX_REDIRECT_PATH=/webex-oauth
MY_WEBEX_SCOPES=spark%3Akms%20spark%3Aall
```
1. You should change the ```UNIQUE_COOKIE_SECRET``` value to some unique alphabetical string.
2. You may change the port (optional - may depend on what port your ngrok tunnel uses to forward requests)
3. You will need to use a baseurl that is secured with https.  I recommend using [ngrok](https://ngrok.com/) if you want to tunnel directly to your personal computer.<br/>
  If you prefer to use ```localhost``` instead of ngrok, then you will need an SSL cert (this is not required if you are using a service like ngrok).  Checkout this answer on [stackoverflow](https://stackoverflow.com/a/13472397) for information about how to use an SSL cert with python-tornado.

I recommend **not** changing ```MY_WEBEX_REDIRECT_PATH``` nor ```MY_WEBEX_SCOPES```
The following instructions assume you do not change these values.

1. To create (register) a Webex integration, click [here.](https://developer.webex.com/my-apps)
2. Click Create App.
3. Select Integration<br/>
  ![image](https://user-images.githubusercontent.com/19175490/134589420-260c6df1-c181-4ed0-b97c-b9f9093649aa.png)
4. Fill in the required fields. Name and Images can be set to anything.  
  **redirect_uri** should be set to your ngrok tunnel or localhost:PORT followed by /webex-oauth. For examples,
  * https://1234.eu.ngrok.io/webex-oauth
  * https://localhost:8000/webex-oauth
5. In the large scopes section, select the scope ```spark:all```<br/>
  ![image](https://user-images.githubusercontent.com/19175490/134589195-cce709f1-4d52-47d4-8583-3accfbd21aa5.png)
6. When you create it, you will be given a ```client_id``` and ```client_secret``` you should use to fill in the corresponding values for:
```
MY_WEBEX_CLIENT_ID=
MY_WEBEX_SECRET=
```

### Optional Environment Variables
```
#MY_ZOOM_CLIENT_ID=
#MY_ZOOM_SECRET=
#MY_ZOOM_REDIRECT_PATH=/zoom-oauth

#MY_AZURE_CLIENT_ID=
#MY_AZURE_SECRET=
#MY_AZURE_REDIRECT_PATH=/azure-oauth
#MY_AZURE_SCOPES=user.read
```
If you want to test [ZOOM](https://marketplace.zoom.us/develop/create) or [AZURE](https://portal.azure.com/#blade/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/RegisteredApps) integrations, you can uncomment these variables.  You will need to fill in the appropriate values when you register an app on those platforms.  When registering on those platforms, remember to set your redirect_uri values as the full url, like:
* https://1234.eu.ngrok.io/azure-oauth
* i.e. https://yourserver.com + MY_*PLATFORM*_REDIRECT_PATH

## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- CONTACT -->

## Contact
Please contact us at wxsd@external.cisco.com
