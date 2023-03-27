# Venture Capital Portfolio Management Suite

**Project title:** Venture Capital Portfolio Management Suite

**Name of the software:** VCPMS

## Team Kinkajou

The members of the team are:

- Kwan Yui Chiu
- Reibjok Othow
- Saadh Zahid
- Kriyes Mahendra
- Kabir Suri
- Adnan Turkay
- Chin Wan
- Chin Kan Yeung
- Fergan Yalim
- Francis Yip

## Project structure

The project is called `vcpms` (Venture Capital Portfolio Management Suite). It currently consists of a single
app `portfolio` where all functionality resides.

## Deployed version of the application

The deployed version of the application can be found at *[http://szahid29a.pythonanywhere.com/](http://szahid29a.pythonanywhere.com/)*.

Credentials for accessing different types of user accounts:
  - Staff account (has access to all components of the software):
    - Username: petra.pickles@example.org
    - Password: Password123
  - User account (has limited visibility of the components):
    - Username: john.doe@example.org
    - Password: Password123
  - Superuser account (accessed via the [Django administrator panel](http://szahid29a.pythonanywhere.com/admin))
    - Username: wayrasuperuser@example.org
    - Password: Superuser123!

## Installation instructions

To install the software and use it in your local development environment, you must first set up and activate a local
development environment. From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the database:

```
$ python3 manage.py migrate
```

## Testing instructions

Seed the development database with:

```
$ python3 manage.py seed
```

Remove all testing data from the database with:

```
$ python3 manage.py unseed
```

Run all tests with:

```
$ python3 manage.py test
```

## Sources

The packages used by this application are specified in `requirements.txt`

This project uses [fileicon.css](https://github.com/picturepan2/fileicon.css)
by [picturepan2](https://github.com/picturepan2):

- Copyright (c) 2014-2015 Picturepan2. MIT Licensed,
  see [LICENSE](https://github.com/AdnanTurkay/team-kinkajou/blob/main/portfolio/static/css/LICENSE) for details.
