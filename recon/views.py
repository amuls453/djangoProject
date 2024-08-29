from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import LoanApplicationForm, ReconForm
from .models import LoanApplication
import pandas as pd
import os

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Wrong username or password.")
        else:
            form.add_error(None, "Wrong username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def home(request):
    return render(request, 'home.html')

def recon_view(request):
    if request.method == 'POST':
        form = ReconForm(request.POST, request.FILES)
        if form.is_valid():
            bank_file = request.FILES['bank_file']
            vendor_file = request.FILES['vendor_file']

            fs = FileSystemStorage()
            bank_filename = fs.save(bank_file.name, bank_file)
            vendor_filename = fs.save(vendor_file.name, vendor_file)

            bank_file_path = os.path.join(settings.MEDIA_ROOT, bank_filename)
            vendor_file_path = os.path.join(settings.MEDIA_ROOT, vendor_filename)

            report_path = reconcile(bank_file_path, vendor_file_path)

            return render(request, 'result.html', {
                'report_url': fs.url(report_path)
            })
    else:
        form = ReconForm()
    return render(request, 'upload.html', {'form': form})

def reconcile(bank_file_path, vendor_file_path):
    bank_data = pd.read_excel(bank_file_path)
    vendor_data = pd.read_excel(vendor_file_path)

    same_day, previous_day = recon_transactions(bank_data, vendor_data)

    report_filename = 'recon_report.xlsx'
    report_path = os.path.join(settings.MEDIA_ROOT, report_filename)
    with pd.ExcelWriter(report_path) as writer:
        same_day.to_excel(writer, sheet_name='Same Day')
        previous_day.to_excel(writer, sheet_name='Previous Day')

    return report_filename

def recon_transactions(bank_df, vendor_df):
    merged = pd.merge(bank_df, vendor_df, how='inner', on=['Transaction Date', 'Transaction ID'])
    unmatched = bank_df[~bank_df['Transaction ID'].isin(merged['Transaction ID'])]
    previous_day = vendor_df.copy()
    previous_day['Transaction Date'] = previous_day['Transaction Date'] + pd.Timedelta(days=1)
    previous_merged = pd.merge(unmatched, previous_day, how='inner', on=['Transaction Date', 'Transaction ID'])
    return merged, previous_merged

def loan(request):
    return render(request, 'loan_registration.html')

def loan_registration(request):
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'loan_registration.html', {'form': LoanApplicationForm(), 'success': True})
        else:
            print(form.errors)  # Print errors to console for debugging
    else:
        form = LoanApplicationForm()

    return render(request, 'loan_registration.html', {'form': form})

def loan_details(request):
    loans = LoanApplication.objects.all()
    return render(request, 'loan_details.html', {'loans': loans})

def loan_dept(request):
    return render(request, 'loan_dept.html')
