import requests
import json

BASE_URL = 'http://localhost:8000/'  # Update with your API base URL
session = requests.Session()  # Create a session object to maintain the connection and cookies
CATEGORY_CHOICES = [
        ('pol', 'Politics'),
        ('art', 'Art'),
        ('tech', 'Technology'),
        ('trivia', 'Trivia'),
    ]
REGION_CHOICES = [
        ('uk', 'UK'),
        ('eu', 'EU'),
        ('w', 'World'),
    ]

def login(input_username, password):
    url = BASE_URL + 'login/'
    data = {'username': input_username, 'password': password}
    response = session.post(url, data=data)
    if response.status_code == 200:
        print(f'Logged in as {input_username}')
        return True
    else:
        print('Login failed:', response.text)
        return False
    
def perform_logout():
    url = BASE_URL + 'logout/'
    response = session.post(url)  # Use session.post instead of requests.post
    if response.status_code == 200:
        print(f'Logged out')
        return True
    else:
        print('Logout failed')
        return False

def post_story():
    if session.cookies.get('sessionid'):
        url = BASE_URL + 'stories/'
        headline = input('Enter headline: ')
        print('Valid categories:', [choice[0] for choice in CATEGORY_CHOICES])
        category = input('Enter category: ')
        print('Valid regions:', [choice[0] for choice in REGION_CHOICES])
        region = input('Enter region: ')
        details = input('Enter details: ')
        
        # Create a dictionary with the JSON data
        data = {
            'headline': headline,
            'category': category,
            'region': region,
            'details': details
        }
        
        # Convert the dictionary to a JSON string
        json_data = json.dumps(data)
        
        # Set the Content-Type header to indicate JSON payload
        headers = {'Content-Type': 'application/json'}
        
        # Send the JSON payload with the headers
        response = session.post(url, data=json_data, headers=headers)
        
        if response.status_code == 201:
            print('Story posted successfully')
        else:
            print(f'Failed to post story. Status code: {response.status_code}')
            print(f'Response: {response.text}')
    else:
        print('Not logged in')

def get_stories():
    print('Enter the criteria to get stories')
    print('Valid categories:', [choice[0] for choice in CATEGORY_CHOICES], ' or * for ALL')
    category = input('Enter category: ')
    print('Valid regions:', [choice[0] for choice in REGION_CHOICES], ' or * for ALL')
    region = input('Enter region: ')
    date = input('Enter date (YYYY-MM-DD) or * for ALL: ')

    url = BASE_URL + 'stories/'
    data = {
        'story_cat': category,
        'story_region': region,
        'story_date': date
    }
    response = requests.get(url, params=data)
    if response.status_code == 200:
        stories = response.json().get('stories')
        for story in stories:
            print(story)  # Do something with each story
    elif response.status_code == 404:
        print('No stories found matching the criteria')
    else:
        print(f'Failed to get stories. Status code: {response.status_code}')

def delete_story(key):
    url = BASE_URL + f'stories/{key}/'
    response = session.delete(url)
    if response.status_code == 200:
        print('Story deleted successfully')
    else:
        print(f'Failed to delete story. Status code: {response.status_code}')
        print(f'Response: {response.text}')

def main():
    while True:
        command = input('Enter command (login, logout, post, get, delete): ')
        if command.lower() == 'login':
            if session.cookies.get('sessionid'):  # Check if the session cookie exists
                print(f'Already logged in as {session.cookies.get("sessionid")}')
            else:
                input_username = input('Enter username: ')
                password = input('Enter password: ')
                login(input_username, password)
        elif command.lower() == 'logout':
            if session.cookies.get('sessionid'):  # Check if the session cookie exists
                perform_logout()
            else:
                print('Not logged in')
        elif command.lower() == 'post':
            post_story()
        elif command.lower() == 'get':
            get_stories()
        elif command.lower() == 'delete':
            key = input('Enter the story key to delete: ')
            delete_story(key)
        else:
            print('Invalid command')

if __name__ == '__main__':
    main()
