from django.db import models

class LoanApplication(models.Model):
    PERSONAL = 'Personal'
    INSTITUTIONAL = 'Institutional'

    LOAN_TYPE_CHOICES = [
        (PERSONAL, 'Personal'),
        (INSTITUTIONAL, 'Institutional'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    loan_type = models.CharField(max_length=50, choices=LOAN_TYPE_CHOICES)
    govt_id_type = models.CharField(max_length=100)
    govt_id_number = models.CharField(max_length=100)
    govt_id_upload = models.ImageField(upload_to='govt_ids/')
    photo_capture = models.ImageField(upload_to='photos/', null=True, blank=True)
    home_coordinates = models.CharField(max_length=100)
    collateral_type = models.CharField(max_length=50)
    collateral_coordinates = models.CharField(max_length=100, null=True, blank=True)
    collateral_details = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
# Create your models here.
