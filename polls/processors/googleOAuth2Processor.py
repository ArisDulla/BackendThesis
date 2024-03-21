from django.conf import settings
import requests


class GoogleOAuth2Processor:
    def __init__(self):
        self._oauthKey = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
        self._oauthSecret = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET

    def _convert_token(self, access_token):

        data = {}

        url = settings.COVERT_TOKEN_URI

        data2 = {
            "grant_type": "convert_token",
            "client_id": self._oauthKey,
            "client_secret": self._oauthSecret,
            "backend": "google-oauth2",
            "token": access_token,
        }

        response = requests.post(url, data=data2)
        data2 = response.json()

        data["refresh"] = data2.get("refresh_token")
        data["access"] = data2.get("access_token")

        return data

    def _get_info_profile(self, access_token):

        # Make a request to fetch the user's profile information
        #
        # https://www.googleapis.com/oauth2/v1/userinfo
        #
        profile_endpoint = settings.GOOGLE_USER_INFO_URI
        headers = {"Authorization": f"Bearer {access_token}"}

        profile_response = requests.get(profile_endpoint, headers=headers)
        return profile_response

    def _exchangeTokenForToken(self, code):

        # Prepare the request parameters to exchange the authorization code for an access token
        #
        # https://oauth2.googleapis.com/token
        #
        token_endpoint = settings.GOOGLE_TOKEN_URI
        token_params = {
            "code": code,
            "client_id": self._oauthKey,
            "client_secret": self._oauthSecret,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,  # Must match the callback URL configured in your Google API credentials
            "grant_type": "authorization_code",
        }

        # Make a POST request to exchange the authorization code for an access token
        response = requests.post(token_endpoint, data=token_params)

        return response
