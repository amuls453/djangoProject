from django.template.context_processors import static
from django.urls import path
from django.shortcuts import redirect
from django.conf.urls.static import static

from djangoProject import settings
from .views import user_login, home, recon_view, loan, loan_dept, loan_details, loan_registration

urlpatterns = [
    path('', lambda request: redirect('login/')),
    path('login/', user_login, name='login'),
    path('home/', home, name='home'),
    path('upload/', recon_view, name='upload'),
    path('loan_registration/',loan, name='loan_registration'),
    path('submit_loan_registration/', loan_registration, name='submit_loan_registration'),
    path('loan_details/', loan_details, name='loan_details'),
    path('loandept/', loan_dept, name='loan_dept'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)