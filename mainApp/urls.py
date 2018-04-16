from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from mainApp import views


router = DefaultRouter()
router.register(r'groups', views.GroupViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'references', views.ReferenceViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]

#urlpatterns = [
#    url(r'^auth|auth.html$', views.AuthView.as_view(), name='AuthView'),
#    url(r'^api-auth', include('rest_framework.urls', namespace='rest_framework')),
#    url(r'^main|main.html$', views.MainView.as_view(), name='MainView'),
#    url(r'^reg|reg.html$', views.RegView.as_view(), name='RegView'),
#    url(r'^|index|index.html$', views.IndexView.as_view(), name='index'),
#]
