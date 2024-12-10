# Venture Capital Portfolio Management Suite

**Project title:** Venture Capital Portfolio Management Suite

**Name of the software:** VCPMS

**Project Description:** Developed an application for our client Wayra Telefonica which allows Wayra to unify key information regarding companies and 
stakeholders.

![image](https://user-images.githubusercontent.com/86085628/228028111-4ea74de7-ca0b-417a-8a0c-0bb8602cc1e1.png)
![image](https://user-images.githubusercontent.com/86085628/228028198-8942cae7-8a65-4d34-b02e-377a6214e735.png)
![image](https://user-images.githubusercontent.com/86085628/228028250-6553a653-900f-43a7-969f-cbfa0685914a.png)
![image](https://user-images.githubusercontent.com/86085628/228028311-7b127c1a-42ce-4484-a30b-797acb5f8bf1.png)
![image](https://user-images.githubusercontent.com/86085628/228028389-4052e4d7-0120-42bb-ad6e-5f0df131a30b.png)
![image](https://user-images.githubusercontent.com/86085628/228028434-62e8477c-b3e1-4003-a7b4-366e850d26a6.png)



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
  
  
## Note

Application was migrated from a seperate, private repository. Hence the lack of activity.

