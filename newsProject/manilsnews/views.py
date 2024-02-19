from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

@csrf_exempt  # Disable CSRF for this view
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Authentication successful
            return HttpResponse('Welcome back!')  # Return 200 OK with welcome message
        else:
            # Authentication failed
            return HttpResponse('Login failed', status=401)  # Return 401 Unauthorized with error message
    else:
        return HttpResponse('Method Not Allowed', status=405)  # Return 405 Method Not Allowed for non-POST requests
