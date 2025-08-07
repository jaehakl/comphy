from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('calculate/spectrum/',CalculateSpectrumView.as_view()),
    path('cie/axis/value/',CieAxisValueView.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)