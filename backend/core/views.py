import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import Plan, Subscription, BillingInvoice


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['plan_count'] = Plan.objects.count()
    ctx['plan_monthly'] = Plan.objects.filter(billing_cycle='monthly').count()
    ctx['plan_quarterly'] = Plan.objects.filter(billing_cycle='quarterly').count()
    ctx['plan_annual'] = Plan.objects.filter(billing_cycle='annual').count()
    ctx['plan_total_price'] = Plan.objects.aggregate(t=Sum('price'))['t'] or 0
    ctx['subscription_count'] = Subscription.objects.count()
    ctx['subscription_active'] = Subscription.objects.filter(status='active').count()
    ctx['subscription_past_due'] = Subscription.objects.filter(status='past_due').count()
    ctx['subscription_cancelled'] = Subscription.objects.filter(status='cancelled').count()
    ctx['subscription_total_mrr'] = Subscription.objects.aggregate(t=Sum('mrr'))['t'] or 0
    ctx['billinginvoice_count'] = BillingInvoice.objects.count()
    ctx['billinginvoice_paid'] = BillingInvoice.objects.filter(status='paid').count()
    ctx['billinginvoice_pending'] = BillingInvoice.objects.filter(status='pending').count()
    ctx['billinginvoice_failed'] = BillingInvoice.objects.filter(status='failed').count()
    ctx['billinginvoice_total_amount'] = BillingInvoice.objects.aggregate(t=Sum('amount'))['t'] or 0
    ctx['recent'] = Plan.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def plan_list(request):
    qs = Plan.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(billing_cycle=status_filter)
    return render(request, 'plan_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def plan_create(request):
    if request.method == 'POST':
        obj = Plan()
        obj.name = request.POST.get('name', '')
        obj.billing_cycle = request.POST.get('billing_cycle', '')
        obj.price = request.POST.get('price') or 0
        obj.features = request.POST.get('features', '')
        obj.subscribers = request.POST.get('subscribers') or 0
        obj.status = request.POST.get('status', '')
        obj.trial_days = request.POST.get('trial_days') or 0
        obj.save()
        return redirect('/plans/')
    return render(request, 'plan_form.html', {'editing': False})


@login_required
def plan_edit(request, pk):
    obj = get_object_or_404(Plan, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.billing_cycle = request.POST.get('billing_cycle', '')
        obj.price = request.POST.get('price') or 0
        obj.features = request.POST.get('features', '')
        obj.subscribers = request.POST.get('subscribers') or 0
        obj.status = request.POST.get('status', '')
        obj.trial_days = request.POST.get('trial_days') or 0
        obj.save()
        return redirect('/plans/')
    return render(request, 'plan_form.html', {'record': obj, 'editing': True})


@login_required
def plan_delete(request, pk):
    obj = get_object_or_404(Plan, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/plans/')


@login_required
def subscription_list(request):
    qs = Subscription.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(customer_name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'subscription_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def subscription_create(request):
    if request.method == 'POST':
        obj = Subscription()
        obj.customer_name = request.POST.get('customer_name', '')
        obj.customer_email = request.POST.get('customer_email', '')
        obj.plan_name = request.POST.get('plan_name', '')
        obj.status = request.POST.get('status', '')
        obj.start_date = request.POST.get('start_date') or None
        obj.next_billing = request.POST.get('next_billing') or None
        obj.mrr = request.POST.get('mrr') or 0
        obj.save()
        return redirect('/subscriptions/')
    return render(request, 'subscription_form.html', {'editing': False})


@login_required
def subscription_edit(request, pk):
    obj = get_object_or_404(Subscription, pk=pk)
    if request.method == 'POST':
        obj.customer_name = request.POST.get('customer_name', '')
        obj.customer_email = request.POST.get('customer_email', '')
        obj.plan_name = request.POST.get('plan_name', '')
        obj.status = request.POST.get('status', '')
        obj.start_date = request.POST.get('start_date') or None
        obj.next_billing = request.POST.get('next_billing') or None
        obj.mrr = request.POST.get('mrr') or 0
        obj.save()
        return redirect('/subscriptions/')
    return render(request, 'subscription_form.html', {'record': obj, 'editing': True})


@login_required
def subscription_delete(request, pk):
    obj = get_object_or_404(Subscription, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/subscriptions/')


@login_required
def billinginvoice_list(request):
    qs = BillingInvoice.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(invoice_number__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'billinginvoice_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def billinginvoice_create(request):
    if request.method == 'POST':
        obj = BillingInvoice()
        obj.invoice_number = request.POST.get('invoice_number', '')
        obj.customer_name = request.POST.get('customer_name', '')
        obj.amount = request.POST.get('amount') or 0
        obj.tax = request.POST.get('tax') or 0
        obj.status = request.POST.get('status', '')
        obj.billing_date = request.POST.get('billing_date') or None
        obj.payment_method = request.POST.get('payment_method', '')
        obj.save()
        return redirect('/billinginvoices/')
    return render(request, 'billinginvoice_form.html', {'editing': False})


@login_required
def billinginvoice_edit(request, pk):
    obj = get_object_or_404(BillingInvoice, pk=pk)
    if request.method == 'POST':
        obj.invoice_number = request.POST.get('invoice_number', '')
        obj.customer_name = request.POST.get('customer_name', '')
        obj.amount = request.POST.get('amount') or 0
        obj.tax = request.POST.get('tax') or 0
        obj.status = request.POST.get('status', '')
        obj.billing_date = request.POST.get('billing_date') or None
        obj.payment_method = request.POST.get('payment_method', '')
        obj.save()
        return redirect('/billinginvoices/')
    return render(request, 'billinginvoice_form.html', {'record': obj, 'editing': True})


@login_required
def billinginvoice_delete(request, pk):
    obj = get_object_or_404(BillingInvoice, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/billinginvoices/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['plan_count'] = Plan.objects.count()
    data['subscription_count'] = Subscription.objects.count()
    data['billinginvoice_count'] = BillingInvoice.objects.count()
    return JsonResponse(data)
