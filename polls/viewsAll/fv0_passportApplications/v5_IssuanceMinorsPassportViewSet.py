from ...models import IssuanceMinorsPassportApplication
from ...serializers.fs0_passportApplications.s5_IssuanceMinorsPassportSerializer import (
    IssuanceMinorsPassportSerializer,
)
from .v0__Common__PassportViewSet import CommonPassportViewSet


#
# Issuance Minors Passport
#
class IssuanceMinorsPassportViewSet(CommonPassportViewSet):
    queryset = IssuanceMinorsPassportApplication.objects.all()
    serializer_class = IssuanceMinorsPassportSerializer
