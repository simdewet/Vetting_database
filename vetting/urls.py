from django.urls import path
from . import views
  
app_name = 'vetting'

urlpatterns = [
	path('', views.fields_table, name="fields_table"),
	path('<int:field_ID>/', views.files_table, name="files_table"),
	path('<int:field_ID>/<int:ID>/', views.image_view, name="images"),
	path('user-selected-candidates/', views.candidates_view, name="user_selected_candidates")
]
