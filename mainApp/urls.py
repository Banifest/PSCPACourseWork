from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^auth|auth.html$', views.AuthView.as_view(), name='AuthView'),
    url(r'^|index|index.html$', views.IndexView.as_view(), name='index'),
]
