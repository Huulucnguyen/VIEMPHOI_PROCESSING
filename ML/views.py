from django.shortcuts import render,redirect
from django.db import transaction
from rest_framework.exceptions import APIException
from django.http import HttpResponse 
from .form import *
from .register_form import *
from .CNN import *
from rest_framework.decorators import api_view
from django.conf import settings
# Create your views here.
from rest_framework import viewsets,mixins,generics
from .models import endpoint, MLAlgorithm,MLAlgorithmStatus,MLRequest,PatientXray
from .serializers import EndpointSerializer,MLAlgorithmSerializer,MLAlgorithmStatusSerializer,MLRequestSerializer,PatientXraySerializer
from .models import *
from django.contrib import messages
class endpointViewset(mixins.RetrieveModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = EndpointSerializer
    queryset = endpoint.objects.all()
class MLAlgorithmViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = MLAlgorithmSerializer
    queryset = MLAlgorithm.objects.all()
def deactivate_other_statuses(instance):
    old_statuses = MLAlgorithmStatus.objects.filter(parent_mlalgorithm = instance.parent_mlalgorithm,
                                                    created_at__lt = instance.created_at,
                                                    active = True)
    for i in range(len(old_statuses)):
        old_statuses[i].active = False
    MLAlgorithm.objects.bulk_update(old_statuses,['active'])
class MLAlgorithmStatusViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
    mixins.CreateModelMixin):
    serializer_class = MLAlgorithmSerializer
    queryset = MLAlgorithmStatus.objects.all()
    def perform_create(self,serializer):
        try:
            with transaction.atomic():
                instance = serializer.save(active = True)
                deactivate_other_statuses(instance)
        except Exception as e:
            raise APIException(str(e))
class MLRequestViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
    mixins.UpdateModelMixin):
    serializer_class = MLRequestSerializer
    queryset = MLRequest.objects.all()

def Patient_Xray_View(request,user_id):
    if request.method == 'POST':
        form = PatientXrayForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('resulst',user_id)  
    else:
        form = PatientXrayForm()
    return render(request,'viemphoi/image_upload.html',{'form':form})
def Resulst(request,user_id):
    return HttpResponse("success")
class Xray_input_view(generics.CreateAPIView):
    queryset = PatientXray.objects.all()
    serializer_class = PatientXraySerializer

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        messages.error (request,"Register Fail")
    form = NewUserForm()
    return render(request,template_name = "viemphoi/register.html",context ={"register_form":form})
