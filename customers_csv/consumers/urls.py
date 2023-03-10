from django.urls import path
from .views import ConsumerView

urlpatterns = [
    path('consumers', ConsumerView.as_view()),
]
