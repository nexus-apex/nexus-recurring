from django.contrib import admin
from .models import Plan, Subscription, BillingInvoice

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ["name", "billing_cycle", "price", "subscribers", "status", "created_at"]
    list_filter = ["billing_cycle", "status"]
    search_fields = ["name"]

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ["customer_name", "customer_email", "plan_name", "status", "start_date", "created_at"]
    list_filter = ["status"]
    search_fields = ["customer_name", "customer_email", "plan_name"]

@admin.register(BillingInvoice)
class BillingInvoiceAdmin(admin.ModelAdmin):
    list_display = ["invoice_number", "customer_name", "amount", "tax", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["invoice_number", "customer_name", "payment_method"]
