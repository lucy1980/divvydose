Python = 3.6.1
Flask = 0.12.2

Python app.py

#Endpoint to access specific user merged profile
http://127.0.0.1:5000/api/v1.0/users/<username>

#Endpoint to merge user profile from specific source
http://127.0.0.1:5000/api/v1.0/users/<username>?s1=github&s2=bitbucket