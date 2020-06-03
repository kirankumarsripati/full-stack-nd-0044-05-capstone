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
If the test are success, you will see something like this
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
### Get all Movies
#### Request
`GET /actors`

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
<a name="delete-actors"></a>
<a name="patch-actors"></a>
<a name="get-movies"></a>
<a name="post-movies"></a>
<a name="delete-movies"></a>
<a name="patch-movies"></a>



