from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializer import LogoutSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.http import FileResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings


class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            refresh_token = serializer.validated_data["refresh_token"]

            try:
                RefreshToken(refresh_token).blacklist()
            except TokenError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#
# Download Files for ADMIN PAGE BACKEND
#
@staff_member_required
def download_file(request, fileName, user):

    media = settings.MEDIA_ROOT

    file_path = media + "/" + user + "/" + fileName

    return FileResponse(open(file_path, "rb"), as_attachment=True)
