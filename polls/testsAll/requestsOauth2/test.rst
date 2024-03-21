DRF-Social-OAuth2
====================

Post request .1
------------------

curl -X POST -d "grant_type=convert_token&
client_id=<django-oauth-generated-client_id>&
client_secret=<django-oauth-generated-client_secret>&backend=google-oauth2&
token=<google_token>" http://127.0.0.1:8000/auth/convert-token


GET request .2
------------------

https://accounts.google.com/o/oauth2/v2/auth?client_id=YOUR_CLIENT_ID&
response_type=code&scope=https://www.googleapis.com/auth/userinfo.profile%20https://www.googleapis.com/auth/userinfo.email&
access_type=offline&redirect_uri=YOUR_REDIRECT_URI        


![OAuth2 Authorization Code Flow](https://developers.google.com/static/identity/protocols/oauth2/images/flows/authorization-code.png)
