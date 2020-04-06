from django.urls import path
from . import views
  
app_name = 'candidates'

urlpatterns = [
	path('', views.candidates, name="candidates"),
	path('<int:ID>/', views.candidates_image_view, name="candidates_image")
]