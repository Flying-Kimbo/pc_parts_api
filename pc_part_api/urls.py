"""
URL configuration for pc_part_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from pc_part_api import settings
from pc_part_api.views import *
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static

from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view


schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Parts API",
        default_version="1.0.0",
        description="API documentaion of App",
    ), public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('parts/', PCParts_list, name='pcparts-list'),

    # URL for retrieving an individual PC part
    path('parts/<str:id>/', PCPart_detail, name='pcpart-detail'),

    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)