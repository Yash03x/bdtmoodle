# Float Moodle

This is our course project for the course CS251 offered in Autumn 2021.

We have deployed the website on heroku [at this link](bdtmoodle.heroku.com).

This repo contains the source code.

## Tech/Framework used:

* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [PostgreSQL](https://www.postgresql.org/)
* [Gunicorn](https://gunicorn.org/)
* [dj-database-url](https://pypi.org/project/dj-database-url/)
* [psycopg2](https://pypi.org/project/psycopg2/)
* [pytz](https://pypi.org/project/pytz/)
* [Whitenoise](http://whitenoise.evans.io/en/stable/index.html#)
* [Pandas](https://pandas.pydata.org/)

## Features

* Login and Signup
* Assignments
  - Create an assignment
  - Access an assignment that an other user has created
  - View all the assignments available for you and attempt them
  - Submit feedback for assignments that you created
* Different roles
  - Students
  - Non Editing Teachers (Teaching Assistants)
  - Teachers
* Deadlines and To-Do Lists
* Percentage of course completed
* Email invitation and password update
  - Emails for course invitations and other important announcements and updates
  - Users can change their password and edit their personal details in the profile section using an otp sent to their email id.


## Instructions to run the code 

1. Install all the required packages and softwares by running the following command on your terminal: `pip install requirements.txt`.
2. Download the project folder.
3. [Setup postgreSQL database](https://www.postgresql.org/download/) and enter the correct credentials in the settings.py file in moodle directory.
4. Go inside the project folder and run the following command on your terminal: `python3 manage.py runserver`

# Project by Team BDT

* __Kumar Satyam__ - 200050064
* __Swayam Shashank Chube__ - 200050141
* __Varanasi Sai Teja__ - 200050152
* __Yash Mailapalli__ - 200050160
