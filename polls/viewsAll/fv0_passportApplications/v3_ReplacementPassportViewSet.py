from ...models import ReplacementPassportApplication
from ...serializers.fs0_passportApplications.s3_ReplacementPassportSerializer import (
    ReplacementPassportSerializer,
)
from .v0__Common__PassportViewSet import CommonPassportViewSet


#
# Replacement Passport
#
class ReplacementPassportViewSet(CommonPassportViewSet):
    queryset = ReplacementPassportApplication.objects.all()
    serializer_class = ReplacementPassportSerializer
