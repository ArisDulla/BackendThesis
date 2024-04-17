from ...models import RenewalPassportApplication
from ...serializers.fs0_passportApplications.s2_RenewalPassportSerializer import (
    RenewalPassportSerializer,
)
from .v0__Common__PassportViewSet import CommonPassportViewSet


#
# Renewal Passport
#
class RenewalPassportViewSet(CommonPassportViewSet):
    queryset = RenewalPassportApplication.objects.all()
    serializer_class = RenewalPassportSerializer
