Please make sure all requirement libraries are installed and that the virtual environment is running. 
All code was desined using Python 3.9.6

My domain: ed19mk3.pythonanywhere.com
Username: ammar
Password: password

Please avoid using the Register function as this agency has already been registered.

Locate the directory of client.py and run 'python client.py'
1) login ed19mk3.pythonanywhere.com
This will log the client session and connect to my server. You will then see the url of the connected agency.
You can use the provided username and password which has admin privilages and is also an Author.

2) logout
This will log the current user out. This requires a user to be logged in.

3) post
You must be logged in and connected to a valid agency.
Enter desired headline
Enter desired category from given list
Enter desired region from given list
Enter details of story
e.g.
- Enter command: post
Enter headline: Example
Enter category: pol
Enter region: uk
Enter details: This is and example.

4) news -id=mck01 -cat=art -reg=w -date=01/03/2024
This would get news from my agency that is related to art and world that has been created on or after 01/03/2024
All switches are optional.
Please note how attributes are not ecnlosed in "" e.g. -cat="art" or -id="mck01". Although, this would also work.

4) delete 7
You must be logged in and be the autohor of the desired story.
This would delete story of key 7.

5) list
This presents a list of all agencies in the directory.

6) register
Do not use!