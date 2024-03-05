import requests
import json
import urllib.parse

BASE_URL = 'https://ed19mk3.pythonanywhere.com/'  # Update with your API base URL
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
    url = BASE_URL + 'api/login'
    # Construct the data in application/x-www-form-urlencoded format
    data = {'username': input_username, 'password': password}
    encoded_data = urllib.parse.urlencode(data)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = session.post(url, data=encoded_data, headers=headers)
    print(response.status_code, ': ', response.text)  # Print server response
    
def perform_logout():
    url = BASE_URL + 'api/logout'
    response = session.post(url)  # Use session.post instead of requests.post
    print(response.status_code, ': ', response.text)  # Print server response

def post_story():
    url = BASE_URL + 'api/stories'
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
    print(response.status_code, ': ', response.text)  # Print server response


def get_stories():
    id_input = input('Enter ID of the news service (press Enter for none): ')
    id_switch = id_input.strip().upper() if id_input else None

    print('Enter the criteria to get stories')
    print('Valid categories:', [choice[0] for choice in CATEGORY_CHOICES], ' or * for ALL')
    category = input('Enter category (press Enter for *): ')
    category = category.strip().lower() if category else '*'

    print('Valid regions:', [choice[0] for choice in REGION_CHOICES], ' or * for ALL')
    region = input('Enter region (press Enter for *): ')
    region = region.strip().lower() if region else '*'

    date = input('Enter date (YYYY-MM-DD) or * for ALL (press Enter for *): ')
    date = date.strip().lower() if date else '*'

    if id_switch:
        url = get_agency_url(id_switch)
        if url is None:
            return
        fetch_all_agencies = False
    else:
        url = 'https://newssites.pythonanywhere.com/api/directory/'
        fetch_all_agencies = True

    try:
        # Fetch all agencies if no ID is specified
        if fetch_all_agencies:
            response = requests.get(url)
            if response.status_code == 200:
                agencies = response.json()
                for agency in agencies:
                    agency_url = agency['url']
                    agency_stories_url = f"{agency_url}/api/stories"
                    print("\nFetching stories for", agency_url)
                    try:
                        fetch_stories_for_agency(agency_stories_url, category, region, date)
                    except Exception as e:
                        print('Error fetching stories for', agency_url, ':', e)
            else:
                print('Failed to fetch agencies:', response.status_code)
        else:
            # Fetch stories for the specified ID
            print("\nFetching stories for ", url)
            fetch_stories_for_agency(url, category, region, date)
    except Exception as e:
        print('Error:', e)

def fetch_stories_for_agency(url, category, region, date):
    data = {
        'story_cat': category,
        'story_region': region,
        'story_date': date
    }
    response = requests.get(url, params=data)
    if response.status_code == 200:
        stories = response.json().get('stories')
        if stories:
            for story in stories:
                print('-----------------------------------')
                print(f"Headline: {story.get('headline')}")
                print(f"Category: {story.get('story_cat')}")
                print(f"Region: {story.get('story_region')}")
                print(f"Author: {story.get('author')}")
                print(f"Date: {story.get('story_date')}")
                print(f"Details: {story.get('story_details')}")
                print('-----------------------------------')
        else:
            print('No stories found matching the criteria')
    elif response.status_code == 404:
        print('No stories found matching the criteria')
    else:
        print('Failed to fetch stories. Status code:', response.status_code)

def get_agency_url(id_switch):
    url = 'https://newssites.pythonanywhere.com/api/directory/'
    try:
        # Send a GET request to the server
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response and extract the agency list
            agencies = response.json()
            if agencies:
                for agency in agencies:
                    if agency['agency_code'] == id_switch:
                        return f"{agency['url']}/api/stories"
                print('No agency found using the ID:', id_switch, '\nPlease enter a valid agency ID.\nUse the list command to view the available agencies')
                return None
            else:
                print('No agencies found ~ Agency list is empty.')
                return None
        else:
            # If the request was not successful, print an error message
            print(f'Failed to fetch agency list. Status code: {response.status_code}')
    except Exception as e:
        # If an exception occurs, print the exception
        print(f'Error: {e}')


def delete_story(key):
    url = BASE_URL + f'stories/{key}/'
    response = session.delete(url)
    if response.status_code == 200:
        print('Story deleted successfully')
    else:
        print(f'Failed to delete story. Status code: {response.status_code}')
        print(f'Response: {response.text}')

def list_agency():
    url = 'https://newssites.pythonanywhere.com/api/directory/'
    try:
        # Send a GET request to the server
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response and extract the agency list
            agencies = response.json()
            if agencies:
                print('List of Agencies:')
                for agency in agencies:
                    print(f"Name: {agency['agency_name']}, URL: {agency['url']}, Code: {agency['agency_code']}")
            else:
                print('No agencies found')
        else:
            # If the request was not successful, print an error message
            print(f'Failed to fetch agency list. Status code: {response.status_code}')
    except Exception as e:
        # If an exception occurs, print the exception
        print(f'Error: {e}')

def register_agency(agency_name, agency_url, agency_code):
    url = 'https://newssites.pythonanywhere.com/api/directory/'
    try:
        # Create a dictionary with the JSON data
        data = {
            'agency_name': agency_name,
            'url': agency_url,
            'agency_code': agency_code
        }
        
        # Convert the dictionary to a JSON string
        json_data = json.dumps(data)
        
        # Set the Content-Type header to indicate JSON payload
        headers = {'Content-Type': 'application/json'}
        
        # Send the JSON payload with the headers
        response = requests.post(url, data=json_data, headers=headers)
        
        # Check if the request was successful (status code 201)
        if response.status_code == 201:
            print('Agency registered successfully')
        else:
            # If the request was not successful, print an error message
            print(f'Failed to register agency. Status code: {response.status_code}')
            print(f'Response: {response.text}')
    except Exception as e:
        # If an exception occurs, print the exception
        print(f'Error: {e}')

def main():
    while True:
        command = input('• login\n• logout\n• post\n• news\n• delete\n• list\n• register\n- Enter command: ')
        if command.lower() == 'login':
            if session.cookies.get('sessionid'):  # Check if the session cookie exists
                print(f'Already logged in!')
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
        elif command.lower() == 'news':
            get_stories()
        elif command.lower() == 'delete':
            key = input('Enter the story key to delete: ')
            delete_story(key)
        elif command.lower() == 'list':
            print('Fetching agency list...')
            list_agency()
        elif command.lower() == 'register':
            agency_name = input('Enter agency name: ')
            url = input('Enter agency URL: ')
            agency_code = input('Enter agency code: ')
            register_agency(agency_name, url, agency_code)
        else:
            print('Invalid command')


if __name__ == '__main__':
    main()
