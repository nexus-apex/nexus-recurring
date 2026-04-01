from django.db import models

class Plan(models.Model):
    name = models.CharField(max_length=255)
    billing_cycle = models.CharField(max_length=50, choices=[("monthly", "Monthly"), ("quarterly", "Quarterly"), ("annual", "Annual"), ("lifetime", "Lifetime")], default="monthly")
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    features = models.TextField(blank=True, default="")
    subscribers = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("deprecated", "Deprecated")], default="active")
    trial_days = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Subscription(models.Model):
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField(blank=True, default="")
    plan_name = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("past_due", "Past Due"), ("cancelled", "Cancelled"), ("trialing", "Trialing")], default="active")
    start_date = models.DateField(null=True, blank=True)
    next_billing = models.DateField(null=True, blank=True)
    mrr = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.customer_name

class BillingInvoice(models.Model):
    invoice_number = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255, blank=True, default="")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=[("paid", "Paid"), ("pending", "Pending"), ("failed", "Failed"), ("refunded", "Refunded")], default="paid")
    billing_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.invoice_number
