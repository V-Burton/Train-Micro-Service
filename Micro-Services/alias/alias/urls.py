from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
    path("alias_view", views.alias_view, name="alias_view"),
	path('prometheus/', include("django_prometheus.urls")),
]
