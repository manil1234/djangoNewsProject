from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from .models import Stories, Author
import json
from datetime import datetime

@csrf_exempt  # Disable CSRF for this view
def login_view(request):
    if request.method == 'POST':
        try:
            # Parse form-urlencoded data
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            # Perform authentication
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Authentication successful
                login(request, user)
                return HttpResponse(f'Welcome back {username}!', content_type='text/plain', status=200)  # Return plain text response
            else:
                # Authentication failed
                return HttpResponse('Invalid username or password', content_type='text/plain', status=401)  # Return plain text response
        except Exception as e:
            return HttpResponse(str(e), content_type='text/plain', status=500)  # Return plain text response for server errors
    else:
        return HttpResponse('Method Not Allowed', content_type='text/plain', status=405)  # Return plain text response for non-POST requests

@csrf_exempt  # Disable CSRF for this view
@login_required
def logout_view(request):
    try:
        logout(request)  # Log out the user
        return HttpResponse('Logged out successfully.')  # Return 200 OK with success message
    except:
        return HttpResponse('Not logged in', status=401)  # Return 401 Unauthorized if user is not logged in

@csrf_exempt
def stories_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:  # Check if the user is logged in
            try:
                # Parse the JSON data manually
                data = json.loads(request.body.decode('utf-8'))
                headline = data.get('headline')
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

                # Create Story
                Stories.objects.create(headline=headline, category=category, region=region, details=details, author=author)

                return JsonResponse({'message': 'CREATED'}, status=201)
            except Exception as e:
                return JsonResponse({'message': str(e)}, status=503)
        else:   # If the user is not logged in
            return HttpResponse('User not logged in', content_type='text/plain', status=503)  # Unauthorized
    elif request.method == 'GET':
        try:
            # Extract query parameters from the request
            category = request.GET.get('story_cat', '*').lower()
            region = request.GET.get('story_region', '*').lower()
            date = request.GET.get('story_date', '*')

            # Retrieve stories based on the provided parameters
            if category == '*':
                stories = Stories.objects.all()
            else:
                stories = Stories.objects.filter(category=category)

            if region != '*':
                stories = stories.filter(region=region)

            print(date)
            if date != '*':
                date_obj = datetime.strptime(date, '%d/%m/%Y')
                stories = stories.filter(date__gte=date_obj)

            # Prepare response data
            response_data = []
            for story in stories:
                response_data.append({
                    'key': story.pk,  # Assuming the primary key is used as the unique key
                    'headline': story.headline,
                    'story_cat': story.category,
                    'story_region': story.region,
                    'author': story.author.name,
                    'story_date': str(story.date.strftime('%d/%m/%Y')),  # Convert date to string
                    'story_details': story.details,
                })

            if response_data:
                return JsonResponse({'stories': response_data}, status=200)
            else:
                return JsonResponse({'message': 'No stories found'}, status=404)
        except ValidationError as ve:
            return JsonResponse({'message': str(ve)}, status=400)  # Bad Request
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)  # Internal Server Error
    else:
        return JsonResponse({'message': 'Method Not Allowed'}, status=405)

    
@csrf_exempt
def delete_story(request, key):
    print("\n\n", request.user.is_authenticated, "\n\n")
    if request.user.is_authenticated:
        try:
            # Check if the story exists
            story = Stories.objects.get(pk=key)

            # Check if the logged-in user is the author of the story
            if request.user == story.author.user:
                # Delete the story
                story.delete()
                return JsonResponse({'message': 'Story deleted successfully.'}, status=200)
            else:
                return JsonResponse({'message': 'Unauthorised to delete this story.'}, status=503)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=503)
    else:
        return HttpResponse(f'User not logged in!', content_type='text/plain', status=503)
