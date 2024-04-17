from ...models import TheftOrLossPassportApplication
from ...serializers.fs0_passportApplications.s4_TheftOrLossPassportSerializer import (
    TheftOrLossPassportSerializer,
)
from .v0__Common__PassportViewSet import CommonPassportViewSet


#
# Theft Or Loss Passport
#
class TheftOrLossPassportViewSet(CommonPassportViewSet):
    queryset = TheftOrLossPassportApplication.objects.all()
    serializer_class = TheftOrLossPassportSerializer
