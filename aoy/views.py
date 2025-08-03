from django.shortcuts import render, get_object_or_404, redirect
from .models import Lead
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime

def dashboard_view(request):
    message = ""

    if request.method == "POST":
        name = request.POST.get("name")
        mobile = request.POST.get("mobile")
        location = request.POST.get("location")
        dob = request.POST.get("dob") or None
        height = request.POST.get("height")
        weight = request.POST.get("weight")
        profession = request.POST.get("profession")
        source = request.POST.get("source")
        session_interest = request.POST.get("session_interest")
        enquiry_datetime_raw = request.POST.get("enquiry_datetime") or None
        lead_status = request.POST.get("lead_status")
        priority = request.POST.get("priority")

        selected_goal = request.POST.get("health_goals")
        custom_goal = request.POST.get("custom_health_goal")

        # Parse enquiry_datetime safely
        enquiry_datetime = None
        if enquiry_datetime_raw:
            try:
                enquiry_datetime = datetime.strptime(enquiry_datetime_raw, '%Y-%m-%dT%H:%M')
            except ValueError:
                enquiry_datetime = None  # fallback if user gives wrong format

        # Optional: handle dob parsing too
        if dob:
            try:
                dob = datetime.strptime(dob, '%Y-%m-%d').date()
            except ValueError:
                dob = None

        # Determine final health goal
        health_goal = "Other" if selected_goal == "Other" else selected_goal
        custom_health_goal = custom_goal if selected_goal == "Other" else ""

        Lead.objects.create(
            name=name,
            mobile=mobile,
            location=location,
            dob=dob,
            height=height,
            weight=weight,
            profession=profession,
            source=source,
            session_interest=session_interest,
            enquiry_datetime=enquiry_datetime,
            lead_status=lead_status,
            priority=priority,
            health_goal=health_goal,
            custom_health_goal=custom_health_goal
        )

        message = "Details are submitted."

    return render(request, "dashboard.html", {"message": message})


@login_required(login_url='admin_login')
def admin_dashboard(request):
    leads = Lead.objects.all()

    # Get filter values
    session_filter = request.GET.get('session_interest', 'All')
    status_filter = request.GET.get('lead_status', 'All')
    goal_filter = request.GET.get('health_goal', 'All')
    search_query = request.GET.get('search', '').strip()

    # Apply filters only if not 'All'
    if session_filter != "All":
        leads = leads.filter(session_interest__iexact=session_filter)

    if status_filter != "All":
        leads = leads.filter(lead_status__iexact=status_filter)

    if goal_filter != "All":
        leads = leads.filter(health_goal__iexact=goal_filter)

    # Apply mobile number search (if not empty or 'None')
    if search_query and search_query.lower() != 'none':
        leads = leads.filter(mobile__icontains=search_query)

    context = {
        'leads': leads,
        'session_filter': session_filter,
        'status_filter': status_filter,
        'goal_filter': goal_filter,
        'search_query': search_query,
    }

    return render(request, 'admin.html', context)

def edit_lead(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    if request.method == "POST":
        lead.name = request.POST.get('name')
        lead.mobile = request.POST.get('mobile')
        lead.location = request.POST.get('location')
        lead.dob = request.POST.get('dob') or None
        lead.height = request.POST.get('height')
        lead.weight = request.POST.get('weight')
        lead.profession = request.POST.get('profession')
        lead.source = request.POST.get('source')
        lead.session_interest = request.POST.get('session_interest')
        
        enquiry_datetime = request.POST.get('enquiry_datetime')
        if enquiry_datetime:
            lead.enquiry_datetime = enquiry_datetime
        else:
            lead.enquiry_datetime = timezone.now()  # fallback value

        lead.lead_status = request.POST.get('lead_status')
        lead.priority = request.POST.get('priority')
        lead.health_goal = request.POST.get('health_goals')
        lead.custom_health_goal = request.POST.get('custom_health_goal')

        lead.save()
        return redirect('admin_dashboard')

    return render(request, 'edit_lead.html', {'lead': lead})

def delete_lead(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    lead.delete()
    return redirect('admin_dashboard')

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'admin_login.html')

def admin_logout(request):
    logout(request)
    return redirect('admin_login')
