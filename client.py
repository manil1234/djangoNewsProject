import requests
import json
import urllib.parse
import argparse
# from datetime import datetime
from tabulate import tabulate

BASE_URL = None
# BASE_URL = 'ed19mk3.pythonanywhere.com'  
# BASE_URL = 'http://127.0.0.1:8000/'  
session = requests.Session()  # Create a session object to maintain the connection and cookies
CATEGORY_CHOICES = {
    'pol': 'Politics',
    'art': 'Art',
    'tech': 'Technology',
    'trivia': 'Trivia',
}
REGION_CHOICES = {
    'uk': 'United Kingdom',
    'eu': 'Europe',
    'w': 'World',
}

def login(input_username, password):
    global BASE_URL
    if BASE_URL is None:
        print('Please enter a valid Agency URL')
        return
    
    url = BASE_URL + '/api/login'
    # Construct the data in application/x-www-form-urlencoded format
    data = {'username': input_username, 'password': password}
    encoded_data = urllib.parse.urlencode(data)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        response = session.post(url, data=encoded_data, headers=headers)
    except Exception as e:
        print('Invalid URL: Please enter a valid Agency URL')
        BASE_URL = None
        return
    if response.status_code != 200:
        BASE_URL = None
    print(response.status_code, ': ', response.text)
    
def perform_logout():
    global BASE_URL
    url = BASE_URL + '/api/logout'
    response = session.post(url) 
    if response.status_code == 200:
        BASE_URL = None
    print(response.status_code, ': ', response.text)  # Print server response

def post_story():
    global BASE_URL
    if BASE_URL is None:
        print('Please enter a valid Agency URL')
        return
    
    url = BASE_URL + '/api/stories'
    headline = input('Enter headline: ')
    print('Valid categories:', list(CATEGORY_CHOICES.keys()))
    category_input = input('Enter category: ')
    # Check if the input is a key in the CATEGORY_CHOICES dictionary
    if category_input in CATEGORY_CHOICES:
        category = category_input
    else:
        # Check if the input matches any full category name, if so, get its key
        category = next((key for key, value in CATEGORY_CHOICES.items() if value.lower() == category_input.lower()), None)
        if not category:
            print('Invalid category. Please choose from:', list(CATEGORY_CHOICES.keys()))
            return

    print('Valid regions:', list(REGION_CHOICES.keys()))
    region = input('Enter region: ')
    # Validate user input
    if region not in REGION_CHOICES:
        print('Invalid region. Please choose from:', list(REGION_CHOICES.keys()))
        return
    
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


def get_stories(id_input=None, category="*", region="*", date="*"):
    total_stories = 0  # Counter variable for total fetched stories
    if id_input:
        url = get_agency_url(id_input.upper().strip('"'))
        # url = 'http://127.0.0.1:8000/'
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
                    if total_stories >= 20:  # Check if the limit is reached
                        break
                    agency_url = agency['url']
                    agency_stories_url = f"{agency_url}/api/stories"
                    try:
                        # Increment total stories fetched by the count for this agency
                        count = fetch_stories_for_agency(agency_stories_url, category, region, date)
                        total_stories += count
                    except Exception as e:
                        print('Error fetching stories for', agency_url, ':', e)
            else:
                print('Failed to fetch agencies:', response.status_code)
        else:
            # Fetch stories for the specified ID
            fetch_stories_for_agency(url, category, region, date)
    except Exception as e:
        print('Error:', e)

def fetch_stories_for_agency(url, category, region, date):
    if not date: date = '*' 
    if not category: category = '*'
    if not region: region = '*'
    data = {
        'story_cat': category.strip('"'),
        'story_region': region.strip('"'),
        'story_date': date.strip('"')
    }
    response = requests.get(url, params=data)
    urls = []
    urls.append([url])
    headersURL = ["URL"]
    print(tabulate(urls, headers=headersURL, tablefmt="grid"))
    if response.status_code == 200:
        stories = response.json().get('stories')
        if stories:
            count = min(len(stories), 20)  # Limit to a maximum of 20 stories

            table_data = []
            for story in stories[:count]:
                table_data.append([
                    story.get('key'),
                    story.get('headline'),
                    CATEGORY_CHOICES.get(story.get('story_cat'), 'Unknown'),
                    REGION_CHOICES.get(story.get('story_region'), 'Unknown'),
                    story.get('author'),
                    story.get('story_date'),
                    story.get('story_details')
                ])

            headers = ["Key", "Headline", "Category", "Region", "Author", "Date", "Details"]
            print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
            return count
        else:
            print('No stories found matching the criteria')
            return 0
    elif response.status_code == 404:
        print('No stories found matching the criteria')
        return 0
    else:
        print('Failed to fetch stories. Status code:', response.status_code)
        return 0

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
            print(f'Failed to fetch agency list. Status code: {response.status_code}')
    except Exception as e:
        print(f'Error: {e}')


def delete_story(key):
    global BASE_URL
    if BASE_URL is None:
        print('Please enter a valid Agency URL')
        return
    
    url = BASE_URL + f'/api/stories/{key}'
    response = session.delete(url)
    print(response.status_code, ': ', response.text)

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
            print(f'Failed to fetch agency list. Status code: {response.status_code}')
    except Exception as e:
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
        
        # Set the Content-Type header to JSON payload
        headers = {'Content-Type': 'application/json'}
        
        # Send  JSON payload with  headers
        response = requests.post(url, data=json_data, headers=headers)
        
        # Check if  request was successful
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
    global BASE_URL
    while True:
        print('-------------------------------------------------------------------------------------------------------------------------------------------------')
        if BASE_URL:
            print('Client is connected to:', BASE_URL)
        else:
            print('Client is not connected to an Agency. \nPlease connect to an Agency using the login command. Use -> ed19mk3.pythonanywhere.com')
        command = input('• login\n• logout\n• post\n• news\n• delete\n• list\n• register\n- Enter command: ')
        args = command.split()
        if args[0].lower() == 'login':
            if session.cookies.get('sessionid'):  # Check if the session cookie exists
                print(f'Already logged in!')
            else:
                if len(args) >= 2:
                    input_username = input('Enter username: ')
                    password = input('Enter password: ')
                    BASE_URL = 'https://' + args[1]
                    login(input_username, password)
                else:
                    print('Please enter a agency URL')
        elif args[0].lower() == 'logout':
            if session.cookies.get('sessionid'):  # Check if the session cookie exists
                perform_logout()
            else:
                print('Not logged in')
        elif args[0].lower() == 'post':
            post_story()
        elif args[0].lower() == 'news':
            parser = argparse.ArgumentParser(description='News Service Command Line Interface')
            parser.add_argument('-id', '--id', help='ID of the news service')
            parser.add_argument('-cat', '--category', help='Category of the news')
            parser.add_argument('-reg', '--region', help='Region of the news')
            parser.add_argument('-date', '--date', help='Date of the news')
            args = parser.parse_args(args[1:])
            get_stories(args.id, args.category, args.region, args.date)
        elif args[0].lower() == 'delete':
            if len(args) >= 2:
                delete_story(int(args[1]))
            else:
                print('Please enter the key of the story to delete.')
        elif args[0].lower() == 'list':
            list_agency()
        elif args[0].lower() == 'register':
            agency_name = input('Enter agency name: ')
            url = input('Enter agency URL: ')
            agency_code = input('Enter agency code: ')
            register_agency(agency_name, url, agency_code)
        else:
            print('Invalid command')


if __name__ == '__main__':
    main()
