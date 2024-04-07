from django.shortcuts import render, get_object_or_404, HttpResponse
from upload.models import PDFDocument
from django.views.generic import ListView
from django.http import StreamingHttpResponse
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

@method_decorator(never_cache, name='dispatch')
class DisplayPDFListView(ListView):
    model = PDFDocument
    template_name = 'display_pdfs.html'
    context_object_name = 'documents'

@never_cache
def pdf_detail_view(request, pk):
    document = get_object_or_404(PDFDocument, pk=pk)
    try:
        def pdf_generator():
            with open(document.file.path, 'rb') as pdf_file:
                while True:
                    data = pdf_file.read(1024)
                    if not data:
                        break
                    yield data
        response = StreamingHttpResponse(pdf_generator(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="{document.name}.pdf"' 
        return response
    except FileNotFoundError:
        return HttpResponse("File not found", status=404)
    