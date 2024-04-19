from rest_framework.response import Response
from django.shortcuts import redirect
from django.views.generic.base import View
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from ..permissions.p5_isNotAuthenticated import IsNotAuthenticated
from ..processors.customUserProcessor import CustomUserProcessor
from ..processors.citizensProcessor import CitizensProcessor
from ..processors.googleOAuth2Processor import GoogleOAuth2Processor


#
# SING UP AND LOGIN ONLY FOR CITIZENS
#
# GOOGLE AYTH
#
class GoogleAuthRedirect(View):

    permission_classes = [IsNotAuthenticated]

    def get(self, request):

        client_id = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
        response_type = "code"
        #
        # scope https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email
        #
        scope = settings.GOOGLE_SCOPE
        access_type = "offline"
        redirect_uri = settings.GOOGLE_REDIRECT_URI
        #
        # URL https://accounts.google.com/o/oauth2/v2/auth?
        #
        redirect_url = (
            f"{settings.GOOGLE_OAUTH2_URI}"
            f"client_id={client_id}&"
            f"response_type={response_type}&"
            f"scope={scope}&"
            f"access_type={access_type}&"
            f"redirect_uri={redirect_uri}"
        )

        return redirect(redirect_url)


#
# REDIRECT URI VIEW GOOGLE
#
class GoogleRedirectURIView(APIView):
    permission_classes = [IsNotAuthenticated]

    def get(self, request):

        # 0. Extract the authorization code from the request URL
        code = request.GET.get("code")

        if code:

            _googleOAuth2Processor = GoogleOAuth2Processor()

            #
            # 1.POST Make a POST request to exchange the authorization code for an access token
            #
            response = _googleOAuth2Processor._exchangeTokenForToken(code)

            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get("access_token")

                if access_token:

                    #
                    # 2. GET www.googleapis.com/oauth2/v1/userinfo ( user's profile information )
                    #
                    profile_response = _googleOAuth2Processor._get_info_profile(
                        access_token
                    )
                    profile_data = profile_response.json()

                    if profile_response.status_code == 200:

                        #
                        # 3. POST http://127.0.0.1:8000/auth/convert-token
                        #
                        data = _googleOAuth2Processor._convert_token(access_token)

                        _customUserProcessor = CustomUserProcessor()

                        #
                        # 4. Returns the user ID if the user exists
                        #
                        idOfUser = _customUserProcessor._user_exists(
                            profile_data["email"]
                        )

                        _citizensProcessor = CitizensProcessor()

                        #
                        # 5. Check if citizen exists based on idUser
                        #
                        citizen = _citizensProcessor._cityzens_exists(idOfUser)
                        if not citizen:
                            #
                            # 6.5 IF NOT EXIST SING UP ( create cityzen )
                            #
                            _citizensProcessor._create_cityzen(idOfUser)

                            message = "Account has been created successfully."
                        else:
                            #
                            # 6.5 ELSE LOGIN
                            #
                            message = "Welcome back!"

                        #
                        # 7. RETURN refresh AND access TOKENS
                        #
                        return Response(
                            {"message": message, "data": data},
                            status=response.status_code,
                        )

        return Response(
            {"error": "Failed to fetch profile information"},
            status=status.HTTP_400_BAD_REQUEST,
        )
