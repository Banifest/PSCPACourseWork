from django.conf.urls import url
from django.urls import include, NoReverseMatch
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

NoReverseMatch()
from mainApp import views
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='Reference API')


router = DefaultRouter()
router.register(r'users', views.UserViewSet)

group_router = NestedSimpleRouter(router, r'users', lookup='users')
group_router.register(r'groups', views.GroupViewSet, base_name='groups')

ref_router = NestedSimpleRouter(router, r'users', lookup='users')
ref_router.register(r'references', views.ReferenceViewSet, base_name='references')

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api/', include(group_router.urls)),
    url(r'^api/', include(ref_router.urls)),
]

