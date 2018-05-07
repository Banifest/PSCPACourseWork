from django.conf.urls import url
from django.urls import include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from mainApp import views

from rest_framework_swagger.views import get_swagger_view
schema_view = get_schema_view(
   openapi.Info(
      title="Reference API",
      default_version='v1',
      description="Reference manager",
      #terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="banifest@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   validators=['flex', 'ssv'],
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'users', views.UserViewSet)

group_router = NestedSimpleRouter(router, r'users', lookup='users')
group_router.register(r'groups', views.GroupViewSet, base_name='groups')

ref_router = NestedSimpleRouter(router, r'users', lookup='users')
ref_router.register(r'references', views.ReferenceViewSet, base_name='references')

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=None), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api/users/login', views.user_login),
    #url(r'^api/', schema_view),
    #url(r'^api/users/', include('rest_framework.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api/', include(group_router.urls)),
    url(r'^api/', include(ref_router.urls)),
]

