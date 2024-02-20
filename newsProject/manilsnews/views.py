from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from .models import Stories, Author
import json

@csrf_exempt  # Disable CSRF for this view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Authentication successful
            login(request, user)
            return HttpResponse('Welcome back ' + username + '!')  # Return 200 OK with welcome message
        else:
            # Authentication failed
            return HttpResponse('Login failed', status=401)  # Return 401 Unauthorized with error message
    else:
        return HttpResponse('Method Not Allowed', status=405)  # Return 405 Method Not Allowed for non-POST requests

@csrf_exempt  # Disable CSRF for this view
@login_required
def logout_view(request):
    try:
        logout(request)  # Log out the user
        return HttpResponse('Logged out successfully.')  # Return 200 OK with success message
    except:
        return HttpResponse('Not logged in', status=401)  # Return 401 Unauthorized if user is not logged in

@csrf_exempt
@login_required
def post_story(request):
    print(request.user.username + ' is trying to post') # Print the logged-in user
    print(request.POST)  # Print the POST data
    if request.method == 'POST':
        try:
            # Parse the JSON data manually
            data = json.loads(request.body.decode('utf-8'))
            headline = data.get('headline')
            print(data.get('category'))
            print(data.get('region'))
            category = data.get('category').lower()
            region = data.get('region').lower()
            details = data.get('details')

            # Validate category and region
            if category not in [choice[0] for choice in Stories.CATEGORY_CHOICES]:
                raise ValidationError('Invalid category')
            if region not in [choice[0] for choice in Stories.REGION_CHOICES]:
                raise ValidationError('Invalid region')

            # Get or create Author
            author_user = request.user  # Get the logged-in user
            author, created = Author.objects.get_or_create(user=author_user, defaults={'name': author_user.username})

            # Create SStory
            Stories.objects.create(headline=headline, category=category, region=region, details=details, author=author)

            return JsonResponse({'message': 'CREATED'}, status=201)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=503)
    else:
        return JsonResponse({'message': 'Method Not Allowed'}, status=405)