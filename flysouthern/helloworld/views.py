from django.http import HttpResponse

# Create your views here.
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated


def hello_world(request):
    return HttpResponse("Hello, World")


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def hello_authenticated_user(request):
    return HttpResponse("Hello, %s" % request.user.email)

