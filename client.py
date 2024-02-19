import requests

BASE_URL = 'http://localhost:8000/'  # Update with your API base URL

def login(username, password):
    url = BASE_URL + 'login/'
    data = {'username': username, 'password': password}
    response = requests.post(url, data=data)
    print(response.text)
    
def perform_logout():
    url = BASE_URL + 'logout/'
    response = requests.post(url)
    print(response.text)

def main():
    while True:
        command = input('Enter command (login, logout): ')
        if command.lower() == 'login':
            username = input('Enter username: ')
            password = input('Enter password: ')
            login(username, password)
        elif command.lower() == 'logout':
            perform_logout()
        else:
            print('Invalid command')

if __name__ == '__main__':
    main()
