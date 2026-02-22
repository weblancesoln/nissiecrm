"""
Lead model for Nissie Ideal Shelters Real Estate CRM.
"""
from django.db import models
from django.contrib.auth.models import User


class Lead(models.Model):
    """Real estate lead/prospect with full tracking."""

    COLOR_CHOICES = [
        ('', 'No Color'),
        ('#28a745', 'Green - Hot Lead'),
        ('#ffc107', 'Yellow - Warm Lead'),
        ('#17a2b8', 'Blue - New'),
        ('#6c757d', 'Gray - Cold'),
        ('#dc3545', 'Red - Urgent'),
        ('#e83e8c', 'Pink - Follow Up'),
        ('#fd7e14', 'Orange - Interested'),
        ('#20c997', 'Teal - Qualified'),
    ]

    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('proposal', 'Proposal Sent'),
        ('negotiation', 'Negotiation'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    point_of_contact = models.CharField(max_length=200, blank=True, help_text='Person or channel they came from')
    prospect_response = models.TextField(blank=True, help_text='Their response or feedback')
    remarks = models.TextField(blank=True, help_text='Internal notes')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    color_code = models.CharField(max_length=20, choices=COLOR_CHOICES, blank=True)
    source = models.CharField(max_length=100, blank=True, help_text='Lead source e.g. Website, Referral')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_leads', help_text='Staff member responsible for this lead')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_leads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip() or self.first_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.first_name
