from django.urls import path
from django.shortcuts import redirect
from .views import user_login, home, recon_view, loan

urlpatterns = [
    path('', lambda request: redirect('login/')),
    path('login/', user_login, name='login'),
    path('home/', home, name='home'),
    path('upload/', recon_view, name='upload'),
    path('loan_registration/',loan, name='loan_registration'),

]