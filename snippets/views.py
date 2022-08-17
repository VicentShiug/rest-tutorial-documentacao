from http.client import ResponseNotReady
from os import stat
from urllib import response
from django.db import reset_queries
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer

from rest_framework import status, mixins, generics, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

from django.contrib.auth.models import User

from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly

from rest_framework import renderers

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class SnippetViewSet(viewsets.ModelViewSet):
    
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                        IsOwnerOrReadOnly]
    
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
    
    
    
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })
    