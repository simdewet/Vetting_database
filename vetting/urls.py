from django.urls import path
from . import views
  
app_name = 'vetting'

urlpatterns = [
	path('', views.fields_table, name="fields_table"),
	path('<int:field_ID>/', views.files_table, name="files_table"),
	path('<int:field_ID>/<int:ID>/', views.image_view, name="images"),
	path('candidates/', views.candidates, name="candidates"),
	path('candidates/<int:ID>/', views.candidates_image_view, name="candidates_image")
]

#path('<int:field_ID>/<int:ID>/', views.images, name="images")
#path('<int:field_ID>/<int:ID>/', image_view.as_view(), name="images")