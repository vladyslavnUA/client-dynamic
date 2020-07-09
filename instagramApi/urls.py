from django.urls import path, include
from . import views

app_name = 'instagram'

urlpatterns = [
    path('instagram/<str:username>/<str:page_id>/<str:token>', views.IndexView.as_view(), name='index'),
]