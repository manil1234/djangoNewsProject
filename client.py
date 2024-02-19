import requests

BASE_URL = 'http://localhost:8000/'  # Update with your API base URL

def login(username, password):
    url = BASE_URL + 'login/'
    data = {'username': username, 'password': password}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print(response.text)
    else:
        print(response.text)

def main():
    command = input('Enter command (login): ')
    if command.lower() == 'login':
        username = input('Enter username: ')
        password = input('Enter password: ')
        login(username, password)
    else:
        print('Invalid command')

if __name__ == '__main__':
    main()
