from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CustomerProfile, CustomerKYC, CustomerActivity

# Create your views here.

@api_view(['GET'])
def api_root(request):
    """
    Customers API Root - Available endpoints
    """
    return Response({
        'message': 'MTT Gateway - Customers API',
        'version': '1.0',
        'endpoints': {
            'profiles': '/api/customers/profiles/',
            'kyc': '/api/customers/kyc/',
            'activities': '/api/customers/activities/',
        },
        'description': 'User profiles, KYC verification, and activity tracking'
    })

@api_view(['GET'])
def customer_profiles_list(request):
    """
    List customer profiles
    """
    profiles = CustomerProfile.objects.all()[:10]
    data = []
    for profile in profiles:
        data.append({
            'id': profile.id,
            'user_id': profile.user.id if profile.user else None,
            'username': profile.user.username if profile.user else None,
            'phone_number': profile.phone_number,
            'verification_status': profile.verification_status,
            'is_active': profile.is_active,
            'created_at': profile.created_at.isoformat()
        })
    
    return Response({
        'count': len(data),
        'results': data
    })

@api_view(['GET'])
def customer_kyc_list(request):
    """
    List customer KYC records
    """
    kyc_records = CustomerKYC.objects.all()[:10]
    data = []
    for kyc in kyc_records:
        data.append({
            'id': kyc.id,
            'customer_id': kyc.customer.id if kyc.customer else None,
            'kyc_level': kyc.kyc_level,
            'verification_status': kyc.verification_status,
            'document_type': kyc.document_type,
            'is_verified': kyc.is_verified,
            'submitted_at': kyc.submitted_at.isoformat() if kyc.submitted_at else None
        })
    
    return Response({
        'count': len(data),
        'results': data
    })

@api_view(['GET'])
def customer_activities_list(request):
    """
    List customer activities
    """
    activities = CustomerActivity.objects.all()[:20]
    data = []
    for activity in activities:
        data.append({
            'id': activity.id,
            'customer_id': activity.customer.id if activity.customer else None,
            'activity_type': activity.activity_type,
            'description': activity.description,
            'ip_address': activity.ip_address,
            'user_agent': activity.user_agent,
            'created_at': activity.created_at.isoformat()
        })
    
    return Response({
        'count': len(data),
        'results': data
    })
