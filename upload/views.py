from django.shortcuts import render, redirect
from django.views import View
from .models import PDFDocument
from .forms import UploadFileForm
from django.contrib.auth import login as user_login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

# Create your views here.


@never_cache
def login(request):
    if request.user.is_authenticated:
        return redirect('upload_pdf')

    error_msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            user_login(request, user)
            return redirect('upload_pdf')
        else:
            error_msg = 'Invalid username or password'
            return render(request, 'login.html', {'error_msg': error_msg})
    
    return render(request, 'login.html')

@login_required
@never_cache
def user_logout(request):
    if not request.user.is_authenticated:
        return redirect('displaypdf')
    
    logout(request)
    return redirect('displaypdf')


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class UploadPDFView(View):
    template_name = 'upload_pdf.html'

    def get(self, request):
        documents = PDFDocument.objects.all()
        form = UploadFileForm() 
        return render(request, self.template_name, {'form': form, 'documents':documents})

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)  # Include request.FILES in POST
        if form.is_valid():
            form.save()
            return redirect('upload_pdf')
        return render(request, self.template_name, {'form': form})

@login_required
@never_cache
def delete_pdf(request, pk):
    try:
        doc = PDFDocument.objects.get(pk=pk)
        doc.delete()
        return redirect('upload_pdf')
    except PDFDocument.DoesNotExist:
        return redirect('upload_pdf')

    
@login_required
@never_cache
def edit_pdf(request, pk):
    try:
        doc = PDFDocument.objects.get(pk=pk)
        documents = PDFDocument.objects.all()
    except PDFDocument.DoesNotExist:
        return redirect('upload_pdf')
    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES, instance=doc)
        if form.is_valid():
            form.save()
            return redirect('upload_pdf')
    else:
        form = UploadFileForm(instance=doc)

    return render(request, 'upload_pdf.html', {'form': form, 'document': doc, 'documents':documents})
    
