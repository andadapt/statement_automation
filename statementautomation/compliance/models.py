from django.db import models
from simple_history.models import HistoricalRecords
from django.urls import reverse
from datetime import timedelta, date
class Portfolio(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    URL_STATUS_CHOICES = [
        ('working', 'Working'),
        ('broken', 'Broken'),
        ('missing', 'Missing'),
        ('authentication', 'Authentication Required'),
    ]

    name = models.CharField(max_length=255)  # Required
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="products")  # Required
    product_url = models.URLField(blank=True, null=True)  # Optional
    statement_url = models.URLField(blank=True, null=True)  # Optional
    product_owner_name = models.CharField(max_length=255, blank=True, null=True)  # Optional
    product_owner_email = models.EmailField(blank=True, null=True)  # Optional, must be valid email
    url_status = models.CharField(
        max_length=20,
        choices=URL_STATUS_CHOICES,
        default='missing',
        blank=True
    )
    comments = models.TextField(blank=True, null=True)  # Optional free text

    def __str__(self):
        return f"{self.name} ({self.portfolio.name})"
    
    def get_absolute_url(self):
        return reverse('compliance:product_detail', args=[str(self.pk)])

    class Meta:
        unique_together = ('name', 'portfolio')  # Enforces unique name per portfolio
        
class Report(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="reports")
    portfolio = models.ForeignKey('Portfolio', on_delete=models.CASCADE, related_name="reports", null=True, blank=True)
    prepared_by_date = models.DateField(blank=True, null=True)
    last_reviewed_date = models.DateField(blank=True, null=True)
    last_tested_date = models.DateField(blank=True, null=True)
    days_since_last_tested = models.IntegerField(blank=True, null=True)
    tested_by = models.CharField(max_length=255, blank=True, null=True)

    # Compliance Booleans
    feedback_header = models.BooleanField(default=False)
    reporting_problems = models.BooleanField(default=False)
    enforcement_procedure = models.BooleanField(default=False)
    technical_information_wording = models.BooleanField(default=False)
    legal_compliance = models.BooleanField(default=False)
    #legal_wording_not_present = models.BooleanField(default=False)

    compliance_status = models.CharField(max_length=50, blank=True, null=True)
    wcag = models.CharField(max_length=50, blank=True, null=True)

    # Contact Info
    feedback_contact_email = models.EmailField(blank=True, null=True)
    feedback_contact_phone = models.CharField(max_length=20, blank=True, null=True)
    reporting_problems_contact_email = models.EmailField(blank=True, null=True)
    reporting_problems_contact_phone = models.CharField(max_length=20, blank=True, null=True)

    non_accessible_content = models.TextField(blank=True, null=True)

    date_report_ran = models.DateField(auto_now_add=True)

    #Overall statement compliance rules in save function
    statement_compliance = models.BooleanField(default=False)

    # History tracking
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        # Set portfolio automatically from product
        if not self.portfolio and self.product:
            self.portfolio = self.product.portfolio

        # Determine legal_compliance from four boolean fields
        self.legal_compliance = all([
            self.feedback_header,
            self.reporting_problems,
            self.enforcement_procedure,
            self.technical_information_wording
        ])

        # Choose review date (last_reviewed or fallback to prepared_by)
        review_date = self.last_reviewed_date or self.prepared_by_date
        is_recent = review_date and (date.today() - review_date <= timedelta(days=365))

        # Compute statement_compliance
        self.statement_compliance = (
            self.wcag == "2.2" and
            self.legal_compliance and
            is_recent
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Report for {self.product.name} - {self.date_report_ran}"
