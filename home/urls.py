from django.urls import path
from .views import DisplayPDFListView, pdf_detail_view

urlpatterns = [
    path('', DisplayPDFListView.as_view(), name='displaypdf'),
    path('pdf_detail/<pk>/', pdf_detail_view, name='pdf_detail'),
]