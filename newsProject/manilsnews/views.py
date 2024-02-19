from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
# @login_required
def logout_view(request):
    try:
        logout(request)  # Log out the user
        return HttpResponse('Logged out successfully.')  # Return 200 OK with success message
    except:
        return HttpResponse('Not logged in', status=401)  # Return 401 Unauthorized if user is not logged in
