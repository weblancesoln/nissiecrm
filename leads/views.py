"""
Views for Nissie Ideal Shelters CRM lead management.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q, Count
from django.contrib.auth.models import User

from .models import Lead
from .forms import LeadForm, LeadUploadForm, StyledAuthenticationForm, StyledUserCreationForm
from .services import import_leads_from_file, export_leads_to_csv, export_leads_to_excel


def register_view(request):
    """User registration."""
    if request.user.is_authenticated:
        return redirect('leads:lead_list')
    if request.method == 'POST':
        form = StyledUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created. Please log in.')
            return redirect('leads:login')
    else:
        form = StyledUserCreationForm()
    return render(request, 'leads/register.html', {'form': form})


def login_view(request):
    """User login."""
    if request.user.is_authenticated:
        return redirect('leads:lead_list')
    if request.method == 'POST':
        form = StyledAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('leads:lead_list')
        messages.error(request, 'Invalid username or password.')
    else:
        form = StyledAuthenticationForm()
    return render(request, 'leads/login.html', {'form': form})


def logout_view(request):
    """User logout - handled by Django auth."""
    from django.contrib.auth import logout
    logout(request)
    return redirect('leads:login')


@login_required
def lead_list(request):
    """List all leads with search, filter, and color coding."""
    queryset = Lead.objects.all()

    # Search
    search = request.GET.get('search', '').strip()
    if search:
        queryset = queryset.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(phone_number__icontains=search) |
            Q(email__icontains=search) |
            Q(remarks__icontains=search) |
            Q(point_of_contact__icontains=search)
        )

    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        queryset = queryset.filter(status=status_filter)

    # Filter by color
    color_filter = request.GET.get('color', '')
    if color_filter:
        queryset = queryset.filter(color_code=color_filter)

    # Filter by staff
    staff_filter = request.GET.get('staff', '')
    if staff_filter:
        queryset = queryset.filter(assigned_to_id=staff_filter)

    # Stats for dashboard
    stats = Lead.objects.aggregate(
        total=Count('id'),
        new=Count('id', filter=Q(status='new')),
        contacted=Count('id', filter=Q(status='contacted')),
        qualified=Count('id', filter=Q(status='qualified')),
        won=Count('id', filter=Q(status='won')),
    )

    # Staff breakdown (users who have assigned leads)
    staff_with_leads = User.objects.filter(
        assigned_leads__isnull=False
    ).annotate(
        lead_count=Count('assigned_leads')
    ).order_by('-lead_count')

    context = {
        'leads': queryset,
        'stats': stats,
        'staff_with_leads': staff_with_leads,
        'search': search,
        'status_filter': status_filter,
        'color_filter': color_filter,
        'staff_filter': staff_filter,
        'color_choices': Lead.COLOR_CHOICES,
        'status_choices': Lead.STATUS_CHOICES,
        'staff_users': User.objects.filter(is_active=True).order_by('username'),
    }
    return render(request, 'leads/lead_list.html', context)


@login_required
def lead_create(request):
    """Create a new lead."""
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.created_by = request.user
            lead.save()
            messages.success(request, f'Lead "{lead.full_name}" created successfully.')
            return redirect('leads:lead_list')
    else:
        form = LeadForm()
    return render(request, 'leads/lead_form.html', {'form': form, 'title': 'Add New Lead'})


@login_required
def lead_edit(request, pk):
    """Edit an existing lead."""
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, f'Lead "{lead.full_name}" updated successfully.')
            return redirect('leads:lead_list')
    else:
        form = LeadForm(instance=lead)
    return render(request, 'leads/lead_form.html', {'form': form, 'title': 'Edit Lead', 'lead': lead})


@login_required
def lead_detail(request, pk):
    """View lead details."""
    lead = get_object_or_404(Lead, pk=pk)
    return render(request, 'leads/lead_detail.html', {'lead': lead})


@login_required
def lead_delete(request, pk):
    """Delete a lead."""
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        name = lead.full_name
        lead.delete()
        messages.success(request, f'Lead "{name}" deleted.')
        return redirect('leads:lead_list')
    return render(request, 'leads/lead_confirm_delete.html', {'lead': lead})


@login_required
def lead_upload(request):
    """Bulk upload leads from CSV or Excel."""
    if request.method == 'POST':
        form = LeadUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            success_count, errors = import_leads_from_file(file, user=request.user)
            if success_count > 0:
                messages.success(request, f'Successfully imported {success_count} lead(s).')
            for err in errors[:5]:  # Show first 5 errors
                messages.warning(request, err)
            if len(errors) > 5:
                messages.warning(request, f'... and {len(errors) - 5} more errors.')
            return redirect('leads:lead_list')
        messages.error(request, 'Please select a valid CSV or Excel file.')
    else:
        form = LeadUploadForm()
    return render(request, 'leads/lead_upload.html', {'form': form})


@login_required
def lead_download_template(request):
    """Download a sample CSV template for uploading leads."""
    import csv
    import io
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'first_name', 'last_name', 'phone_number', 'email', 'point_of_contact',
        'prospect_response', 'remarks', 'status', 'source', 'assigned_to'
    ])
    writer.writerow([
        'John', 'Doe', '+234 800 123 4567', 'john@example.com', 'Website',
        'Interested in 3-bedroom', 'Called back twice', 'new', 'Website', 'username'
    ])
    response = HttpResponse(output.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="leads_template.csv"'
    return response


@login_required
def lead_download(request):
    """Download leads as CSV or Excel."""
    format_type = request.GET.get('format', 'csv')
    queryset = Lead.objects.all()

    # Apply same filters as list view if passed
    search = request.GET.get('search', '').strip()
    if search:
        queryset = queryset.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(phone_number__icontains=search) |
            Q(email__icontains=search)
        )
    status_filter = request.GET.get('status', '')
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    color_filter = request.GET.get('color', '')
    if color_filter:
        queryset = queryset.filter(color_code=color_filter)
    staff_filter = request.GET.get('staff', '')
    if staff_filter:
        queryset = queryset.filter(assigned_to_id=staff_filter)

    if format_type == 'excel':
        try:
            content = export_leads_to_excel(queryset)
        except ImportError:
            messages.error(request, 'Excel export requires openpyxl. Run: pip install openpyxl. Use CSV for now.')
            return redirect('leads:lead_list')
        response = HttpResponse(content, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="nissie_leads.xlsx"'
    else:
        content = export_leads_to_csv(queryset)
        response = HttpResponse(content, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="nissie_leads.csv"'

    return response
