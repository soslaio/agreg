
from django.urls import path, include
from core.urls import corepatterns


urlpatterns = [
    path('', include(corepatterns))
]
