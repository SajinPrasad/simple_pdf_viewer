from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.UploadPDFView.as_view(), name='upload_pdf'),
    path('login/', views.login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('edit_pdf/<pk>/', views.edit_pdf, name='edit_pdf'),
    path('delete_pdf/<pk>/', views.delete_pdf, name='delete_pdf'),
]