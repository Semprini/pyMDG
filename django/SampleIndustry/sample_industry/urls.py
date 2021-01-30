"""sample_industry URL Configuration

"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from rest_framework import permissions

from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from drf_nest.routers import AppRouter


from Test_Domain.urls import urlpatterns as Test_DomainUrls

admin.site.site_title = 'SampleIndustry'
admin.site.site_header = 'SampleIndustry Admin'

schema_view = get_schema_view(
   openapi.Info(
      title="API Schema",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

apps={  
    'Test_Domain':'app-Test_Domain',
}
router = AppRouter( apps=apps )

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^streams', views.streams, name='streams'),	
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
	path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + Test_DomainUrls