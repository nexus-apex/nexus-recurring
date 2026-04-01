from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Plan, Subscription, BillingInvoice
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusRecurring with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexusrecurring.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if Plan.objects.count() == 0:
            for i in range(10):
                Plan.objects.create(
                    name=f"Sample Plan {i+1}",
                    billing_cycle=random.choice(["monthly", "quarterly", "annual", "lifetime"]),
                    price=round(random.uniform(1000, 50000), 2),
                    features=f"Sample features for record {i+1}",
                    subscribers=random.randint(1, 100),
                    status=random.choice(["active", "deprecated"]),
                    trial_days=random.randint(1, 100),
                )
            self.stdout.write(self.style.SUCCESS('10 Plan records created'))

        if Subscription.objects.count() == 0:
            for i in range(10):
                Subscription.objects.create(
                    customer_name=f"Sample Subscription {i+1}",
                    customer_email=f"demo{i+1}@example.com",
                    plan_name=f"Sample Subscription {i+1}",
                    status=random.choice(["active", "past_due", "cancelled", "trialing"]),
                    start_date=date.today() - timedelta(days=random.randint(0, 90)),
                    next_billing=date.today() - timedelta(days=random.randint(0, 90)),
                    mrr=round(random.uniform(1000, 50000), 2),
                )
            self.stdout.write(self.style.SUCCESS('10 Subscription records created'))

        if BillingInvoice.objects.count() == 0:
            for i in range(10):
                BillingInvoice.objects.create(
                    invoice_number=f"Sample {i+1}",
                    customer_name=f"Sample BillingInvoice {i+1}",
                    amount=round(random.uniform(1000, 50000), 2),
                    tax=round(random.uniform(1000, 50000), 2),
                    status=random.choice(["paid", "pending", "failed", "refunded"]),
                    billing_date=date.today() - timedelta(days=random.randint(0, 90)),
                    payment_method=f"Sample {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 BillingInvoice records created'))
