"""
URL configuration for KLAPI project.

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
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from KL_app.views import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

router=routers.SimpleRouter()
router.register('collection',CollectionListViewSet, basename='collection')
router.register('listemodele',ModeleListViewSet,basename='listemodele')
router.register('listeaccessoire',AccessoireListViewSet,basename='listeaccessoire')
router.register('modele',ModeleViewSet,basename='modele')
router.register('accessoire',AccessoireViewSet,basename='accessoire')
###ADMIN###
router.register('admincollection',CollectionAdminViewSet, basename='admincollection')
router.register('adminmodele',ModeleAdminViewSet,basename='adminmodele')
router.register('adminaccessoire',AccessoireAdminViewSet,basename='adminaccessoire')
router.register('cmdmodele',CmdModeleViewset,basename='cmdmodele')
router.register('cmdaccessoire',CmdAccessoireViewset,basename='cmdaccessoire')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api/token/',TokenObtainPairView.as_view(),name='obtain_tokens'),
    path('api/token/refresh/',TokenRefreshView.as_view(),name='refresh_token'),    
  ]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)