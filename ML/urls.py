from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import endpointViewset
from .views import MLAlgorithmViewSet
from .views import MLAlgorithmStatusViewSet
from .views import MLRequestViewSet
from ML.views import *
from ML.login_views import login_request
from django.urls import path
app_name = "ML"
router = DefaultRouter(trailing_slash = False)
router.register(r"endpoints",endpointViewset,basename = "endpoints")
router.register(r"mlalgorithm",MLAlgorithmViewSet,basename = "mlalgorithm")
router.register(r"mlalgorithmstatus",MLAlgorithmStatusViewSet,basename = "mlalgorithmstatus")
router.register(r"mlrequest",MLRequestViewSet,basename = "mlrequest")
urlpatterns = [
    path('image_upload/<int:user_id>/',Patient_Xray_View,name = 'image_upload'),
    path('result/<int:user_id>/',Resulst,name = 'resulst'),
    path('',Xray_input_view.as_view(),name = 'home'),
    path("register/",register_request,name = "register"),
    path("login/",login_request,name = "login"),
    
    url(r"api/v1/", include(router.urls)),
]