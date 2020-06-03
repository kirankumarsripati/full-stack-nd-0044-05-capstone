# Full-Stack Developer Nanodegree Program - Capstone Project

## Content

1. [Motivation](#motivation)
1. [Development](#development)
1. [Unit Testing](#testing)
1. [API Documentation](#api)
1. [Authentication](#authentication)

<a name="motivation"></a>
## Motivation
I was working in the Front End Development for more than a decade. Started career with Adobe Flash and moved to HTML, CSS and JavaScript. Now working as a Angular Developer. I wanted to learn the backend part of the stack from a long time and this Nanodegree helped me to achieve it.

Here I learned below topics
1. Modeling database with `postgres` and `SQLAlchemy`
2. CRUD operations using `Flask`
3. Write test cases for API with `Unittest`
4. Authorization and Roles using Auth0
5. Deploying API to `Heroku`

<a name="#develop-locally"></a>
## Development
### Requirements
1. Python 3
2. Postgres

### Steps
1. Initialize and activate a virtualenv

```bash
$ virtualenv venv
$ source venv/bin/activate
```
2. Install the dependencies
```bash
$ pip install -r requirements.txt
```

3. Add environment variables
```bash
$ export DATABASE_URL=<YOUR_POSTGRES_DB_URL>
$ export DATABASE_TEST_URL=<YOUR_POSTGRES_TEST_DB_URL>
```

4. Setup Auth0

There are existing bearer tokens in `test_app.py` or in `agency-api.postman_collection.json` if you just want to test API, but the problem is that they expire in 24 hours.
For generating fresh tokens, you need a front end, but for this part I choose to develop only API. Fortunately you can use my previous [project front-end](https://github.com/kirankumarsripati/full-stack-nd-0044-03-coffee-shop-full-stack) to generate tokens.

 - First setup your account at Auth0
 - Update config variables with yours in `config.py`
```
AUTH0_DOMAIN = 'dev-jv5b18wv.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'FSND'
```
 - Follow instructions to run front-end - https://github.com/kirankumarsripati/full-stack-nd-0044-03-coffee-shop-full-stack/blob/master/frontend/README.md
 - Once you run the app, click on Login button, if login successful, it will return a token
 - Make sure to set Roles and Permission to the user. For more information, see [Authentication](#authentication)

<a name="#testing"></a>
## Unit Testing
I already created some database records for testing, first drop your testing dp, create testing db and import the `agency.psql` and run the tests.

Below commands assume your test db name is `agency-test`
```
dropdb agency-test
createdb agency-test
psql agency-test < agency.psql
python test_app.py
```
If the test are successful, you will see something like this
```
........................
----------------------------------------------------------------------
Ran 24 tests in 22.966s

OK
```
<a name="#api"></a>
## API Documentation
### Base URL
https://agency-capstone.herokuapp.com/

Each API requires Authentication, for more information, see [Authentication](#authentication)

### Available Endpoints
Here is a short table about which resources exist and which method you can use on them.

                          Allowed Methods
       Endpoints    |  GET |  POST |  DELETE | PATCH  |
                    |------|-------|---------|--------|
      /actors       |  [x] |  [x]  |   [x]   |   [x]  |
      /movies       |  [x] |  [x]  |   [x]   |   [x]  |

### Endpoint Details
1. Actors
- [GET /actors](#get-actors)
- [POST /actors](#post-actors)
- [DELETE /actors](#delete-actors)
- [PATCH /actors](#patch-actors)
2. Movies
- [GET /movies](#get-movies)
- [POST /movies](#post-movies)
- [DELETE /movies](#delete-movies)
- [PATCH /movies](#patch-movies)

<a name="get-actors"></a>
### GET /actors
#### Request
```bash
curl -i -H $HEADERS https://agency-capstone.herokuapp.com/actors
```

#### Response
```bash
HTTP/1.1 200 OK
Connection: keep-alive
Server: gunicorn/20.0.4
Date: Wed, 03 Jun 2020 08:02:47 GMT
Content-Type: application/json
Content-Length: 611
Access-Control-Allow-Headers: Content-Type,Authorization,true
Access-Control-Allow-Methods: GET,PATCH,POST,DELETE,OPTIONS
Access-Control-Allow-Origin: *
Via: 1.1 vegur

{
  "actors": [
    {
      "age": 50,
      "gender": "Male",
      "id": 1,
      "name": "R. Madhavan"
    },
    {
      "age": 55,
      "gender": "Male",
      "id": 2,
      "name": "Aamir Khan"
    },
    {
      "age": 41,
      "gender": "Male",
      "id": 3,
      "name": "Sharman Joshi"
    },
    {
      "age": 33,
      "gender": "Male",
      "id": 4,
      "name": "Ali Fazal"
    },
    {
      "age": 19,
      "gender": "Male",
      "id": 5,
      "name": "Siddharth Nigam"
    },
    {
      "age": 44,
      "gender": "Male",
      "id": 6,
      "name": "Abhishek Bachchan"
    },
    {
      "age": 47,
      "gender": "Male",
      "id": 7,
      "name": "Uday Chopra"
    },
    {
      "age": 63,
      "gender": "Male",
      "id": 8,
      "name": "Jackie Shroff"
    },
    {
      "age": 77,
      "gender": "Male",
      "id": 9,
      "name": "Amitabh Bachchan"
    },
    {
      "age": 77,
      "gender": "Male",
      "id": 10,
      "name": "Amitabh Bachchan"
    }
  ],
  "success": true,
  "total": 11
}
```
<a name="post-actors"></a>
### POST /actors
#### Request
```bash
curl -i -H $HEADERS -H 'Content-Type: application/json' -X POST -d '{ "name": "Test Actor", "age": 56 }' https://agency-capstone.herokuapp.com/actors
```
#### Response
```bash
HTTP/1.1 200 OK
Connection: keep-alive
Server: gunicorn/20.0.4
Date: Wed, 03 Jun 2020 08:16:27 GMT
Content-Type: application/json
Content-Length: 30
Access-Control-Allow-Headers: Content-Type,Authorization,true
Access-Control-Allow-Methods: GET,PATCH,POST,DELETE,OPTIONS
Access-Control-Allow-Origin: *
Via: 1.1 vegur

{"created":15,"success":true}
```

<a name="delete-actors"></a>
### DELETE /actors
#### Request
```bash
curl -i -H $HEADERS -X DELETE https://agency-capstone.herokuapp.com/actors/15
```
#### Response
```bash
HTTP/1.1 200 OK
Connection: keep-alive
Server: gunicorn/20.0.4
Date: Wed, 03 Jun 2020 08:19:52 GMT
Content-Type: application/json
Content-Length: 30
Access-Control-Allow-Headers: Content-Type,Authorization,true
Access-Control-Allow-Methods: GET,PATCH,POST,DELETE,OPTIONS
Access-Control-Allow-Origin: *
Via: 1.1 vegur

{"deleted":15,"success":true}
```
<a name="patch-actors"></a>
### PATCH /actors
#### Request
```bash
curl -i -H $HEADERS -H 'Content-Type: application/json' -X PATCH -d '{ "age": 34 }' https://agency-capstone.herokuapp.com/actors/3
```
#### Response
```bash
HTTP/1.1 200 OK
Connection: keep-alive
Server: gunicorn/20.0.4
Date: Wed, 03 Jun 2020 08:26:14 GMT
Content-Type: application/json
Content-Length: 29
Access-Control-Allow-Headers: Content-Type,Authorization,true
Access-Control-Allow-Methods: GET,PATCH,POST,DELETE,OPTIONS
Access-Control-Allow-Origin: *
Via: 1.1 vegur

{"success":true,"updated":3}
```
<a name="get-movies"></a>
### GET /movies
#### Request
```bash
curl -i -H $HEADERS https://agency-capstone.herokuapp.com/movies
```
#### Response
```bash
HTTP/1.1 200 OK
Connection: keep-alive
Server: gunicorn/20.0.4
Date: Wed, 03 Jun 2020 08:27:55 GMT
Content-Type: application/json
Content-Length: 549
Access-Control-Allow-Headers: Content-Type,Authorization,true
Access-Control-Allow-Methods: GET,PATCH,POST,DELETE,OPTIONS
Access-Control-Allow-Origin: *
Via: 1.1 vegur

{
  "movies": [
    {
      "id": 1,
      "release_year": 2009,
      "title": "3 Idiots"
    },
    {
      "id": 2,
      "release_year": 2019,
      "title": "Rubaru Roshni"
    },
    {
      "id": 3,
      "release_year": 2020,
      "title": "Lal Singh Chaddha"
    },
    {
      "id": 4,
      "release_year": 2017,
      "title": "Secret Superstar"
    },
    {
      "id": 5,
      "release_year": 2018,
      "title": "Thugs of Hindostan"
    },
    {
      "id": 6,
      "release_year": 2016,
      "title": "Dangal"
    },
    {
      "id": 7,
      "release_year": 2015,
      "title": "Dil Dhadakne Do"
    },
    {
      "id": 8,
      "release_year": 2014,
      "title": "PK"
    },
    {
      "id": 9,
      "release_year": 2013,
      "title": "Dhoom 3"
    },
    {
      "id": 10,
      "release_year": 2012,
      "title": "Talaash"
    }
  ],
  "success": true,
  "total": 15
}
```
<a name="post-movies"></a>
### POST /movies
#### Request
```bash
curl -i -H $HEADERS -H 'Content-Type: application/json' -X POST -d '{ "title": "Kabhi Eid Kabhi Diwali", "release_year": 2021 }' https://agency-capstone.herokuapp.com/movies
```
#### Response
```bash
HTTP/1.1 200 OK
Connection: keep-alive
Server: gunicorn/20.0.4
Date: Wed, 03 Jun 2020 08:31:23 GMT
Content-Type: application/json
Content-Length: 30
Access-Control-Allow-Headers: Content-Type,Authorization,true
Access-Control-Allow-Methods: GET,PATCH,POST,DELETE,OPTIONS
Access-Control-Allow-Origin: *
Via: 1.1 vegur

{"created":16,"success":true}
```
<a name="delete-movies"></a>
### DELETE /movies
#### Request
```bash
curl -i -H $HEADERS -X DELETE https://agency-capstone.herokuapp.com/movies/16
```
#### Response
```bash
HTTP/1.1 200 OK
Connection: keep-alive
Server: gunicorn/20.0.4
Date: Wed, 03 Jun 2020 08:32:38 GMT
Content-Type: application/json
Content-Length: 30
Access-Control-Allow-Headers: Content-Type,Authorization,true
Access-Control-Allow-Methods: GET,PATCH,POST,DELETE,OPTIONS
Access-Control-Allow-Origin: *
Via: 1.1 vegur

{"deleted":16,"success":true}
```
<a name="patch-movies"></a>
### PATCH /movies
#### Request
```bash
curl -i -H $HEADERS -H 'Content-Type: application/json' -X PATCH -d '{ "release_year": 2013 }' https://agency-capstone.herokuapp.com/movies/10
```
#### Response
```bash
HTTP/1.1 200 OK
Connection: keep-alive
Server: gunicorn/20.0.4
Date: Wed, 03 Jun 2020 08:34:19 GMT
Content-Type: application/json
Content-Length: 30
Access-Control-Allow-Headers: Content-Type,Authorization,true
Access-Control-Allow-Methods: GET,PATCH,POST,DELETE,OPTIONS
Access-Control-Allow-Origin: *
Via: 1.1 vegur

{"success":true,"updated":10}
```
<a name="authentication"></a>
### Authentication
They are 3 Roles with distinct permission sets:

1. Casting Assistant:
  - GET /actors (read:actors): Can see all actors
  - GET /movies (read:movies): Can see all movies
2. Casting Director (everything from Casting Assistant plus)
  - POST /actors (create:actors): Can create new Actors
  - PATCH /actors (edit:actors): Can edit existing Actors
  - DELETE /actors (delete:actors): Can remove existing Actors from database
  - PATCH /movies (edit:movies): Can edit existing Movies
3. Executive Director (everything from Casting Director plus)
  - POST /movies (create:movies): Can create new Movies
  - DELETE /movies (delete:movies): Can remove existing Movies from database