from ...models import IssuancePassportApplication
from ...serializers.fs0_passportApplications.s1_IssuancePassportSerializer import (
    IssuancePassportSerializer,
)
from .v0__Common__PassportViewSet import CommonPassportViewSet


#
# Issuance Passport
#
class IssuancePassportViewSet(CommonPassportViewSet):
    queryset = IssuancePassportApplication.objects.all()
    serializer_class = IssuancePassportSerializer
