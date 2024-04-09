Djoser
====================

Register a new user:
------------------
curl -X POST http://127.0.0.1:8000/auth/users/ --data 'username=djodafdsser&password=alpine12&email=it21964@hua.gr'
{"email": "", "username": "djoser", "id":1}

Activation
---------------
http://127.0.0.1:8000/auth/users/activation/

ERROR Access user’s details:
------------------------------------
curl -LX GET http://127.0.0.1:8000/auth/users/me/
{"detail": "Authentication credentials were not provided."}

Log in:
------------------------------------
curl -X POST http://127.0.0.1:8000/auth/token/login/ --data 'username=asdacdsqewcvxz&password=alpine12'
{"auth_token": ""}

ERROR Access user’s details again:
------------------------------------
curl -LX GET http://127.0.0.1:8000/auth/users/me/
{"detail": "Authentication credentials were not provided."}

Access is still forbidden but let’s offer the token we obtained:
------------------------------------------------------------------------
curl -LX GET http://127.0.0.1:8000/auth/users/me/ -H 'Authorization: Token 0000'
{"email": "", "username": "djoser", "id": 1}

Log out:
-------------
curl -X POST http://127.0.0.1:8000/auth/token/logout/  --data 'token' -H 'Authorization: Token token'

Reset password ONLY Activated
--------------------------------
curl -X POST http://127.0.0.1:8000/auth/users/reset_password/ --data email=it21964@hua.gr

http://127.0.0.1:8000/auth/users/reset_password_confirm/

JWT
====================
https://djoser.readthedocs.io/en/latest/jwt_endpoints.html

JWT Create
----------
Default URL: /jwt/create/

JWT Refresh
-------------
Default URL: /jwt/refresh/

JWT Verify
-------------
Default URL: /jwt/verify/
