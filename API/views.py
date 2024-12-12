from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from Models.models import Job, JobApplication, Company, Account
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated 
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
# permission_classes 

import json


def jobs(request):
    jobs = Job.objects.all()
    return JsonResponse({"jobs": list(jobs.values())})

@csrf_exempt    
def login(request):
    if request.method == "POST":
        data = request.body.decode('utf-8')
        data = json.loads(data)
        email = data.get('email')
        password = data.get('password')
        print(email, password)
        user = authenticate(request, username=email, password=password)
        
       
        if user:
            login_user(request, user)
            refresh = RefreshToken.for_user(user) 
            return JsonResponse({"message": "Logged in", "refresh": str(refresh), "access": str(refresh.access_token), "user": {"email": user.email, "first_name": user.first_name, "last_name": user.last_name, "role": user.account_type}})         
        else:
            return HttpResponse("Invalid credentials", status=401)  
    return  HttpResponse("Invalid request", status=400)


@csrf_exempt 
def signup(request):
    if request.method == "POST":
        data = request.body.decode('utf-8') 
        data = json.loads(data) 
        account_type = request.GET.get('type')
        if account_type == "employee": 
            print("employee")
            print(data)
            password = data.get('password')
            data['password'] = make_password(password)
            user = Account.objects.create_user(
                username=data.get('email'),
                email=data.get('email'),
                password=data.get('password'),
                account_type="Employee",
                first_name=data.get('firstName'),
                last_name=data.get('lastName'),
                date_of_birth=data.get('birthDate'),
                sex=data.get('sex'),
                address=data.get('address'),
                contact_number=data.get('contactNo')
            )
        elif account_type == "employer": 
            user = Account.objects.create_user(username=data.get('email'), email=data.get('email'), password=data.get('password'), account_type="Employer")
            user.first_name = data.get('company_name')
        else:
            return JsonResponse({"status" : 401,"message": "Invalid account type"})
        
        user.save()
        access_token = RefreshToken.for_user(user)  
        return JsonResponse({"message": "Account created successfully", "access": str(access_token.access_token), "refresh": str(access_token)})
        
        
        
        
@api_view(['POST'])
@csrf_exempt
def refresh_token(request):
    if request.method == "POST":
        data = request.body.decode('utf-8')
        data = json.loads(data)
        refresh = data.get('refresh')
        token = RefreshToken(refresh)
        user = token.user
        access = str(token.access_token)
        return JsonResponse({"access": access})
    return HttpResponse("Invalid request", status=400)
        
        
        
        
  
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_auth(request):
    if request.user.is_authenticated: 
        user = { 
            "id": request.user.id, 
            "username": request.user.username, 
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email, 
            "date_of_birth": request.user.date_of_birth, 
            "role": request.user.account_type,
            "contact_number": request.user.contact_number, 
            "address": request.user.address,
            
        }
        return JsonResponse(user, safe=False) 
    else:
        return JsonResponse({"error": "User not authenticated"}, status=400) 
          
        
        