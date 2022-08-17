from pydoc import visiblename
from urllib.parse import urlparse
from django.urls import path, include
from requests_toolbelt import user_agent
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

from snippets.views import SnippetViewSet, UserViewSet, api_root
from rest_framework import renderers


router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet,basename="snippets")
router.register(r'users', views.UserViewSet,basename="users")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]

snippet_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
snippet_detail = SnippetViewSet.as_view({
    'get':'retrieve',
    'put':'update',
    'patch':'partial_update',
    'delete':'destroy'
    
})
snippet_highlight = SnippetViewSet.as_view({
    'get':'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])
user_list = UserViewSet.as_view({
    'get':'list'
})
user_detail = UserViewSet.as_view({
    'get':'retrieve'
})


urlpatterns = format_suffix_patterns([
    path('', api_root),
    path('snippets/', snippet_list, name='snippet-list'),
    path('snippets/<int:pk>', snippet_detail, name='snippet-detail'),
    path('snippets/<int:pk>/highlight/', snippet_highlight, name='snippet-highlight'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail'),    
      
])

