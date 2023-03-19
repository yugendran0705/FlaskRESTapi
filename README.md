# FlaskRESTapi

Description: A backend service for application in which student selects a course from a list of courses and register for it with all endpoints for basic CRUD operations on registrations and courses database for administration purposes with proper JWT authentication.

Documentation: Documentation for Flask REST API.pdf

To run flask app on linux:

Install Apache.
Get your code onto the server.
Create a python virtual environment for your application and check that you can run your application.
Configure your Web Server Gateway Interface (WSGI) file. This is how your Flask application will talk to Apache.
Set up the Apache configuration for your site.
Carefully define the read/write/execute permissions for different parts of your web application and make use of the Apache user group.

Hit 

> sudo apt-get install apache2 

and then 

> sudo apt-get install libapache2-mod-wsgi-py3.
The next step is to get your code off a GitHub repository and onto the server.
To do that, navigate to the directories typically used for Apache configuration.
Hit 

> cd /var/www/html 

and then 

> sudo git clone <your repository url>

simple way to create an environment from the system python on the server. 
First, switch to the directory that contains your site 

 > cd /var/www/html/your_site_name

Then hit

> python3 -m venv your_site_environment

Ideally, your project code will contain a requirements.txt file that contains all your project dependencies.
Activate your python environment by hitting 

> source/your_site_environment/bin/activate

> pip install -r requirements.txt

Configure your WSGI File
Now, head to your website's directory on the server with 
  
> cd /var/www/html/your_site_name 

and hit 

> touch your_site.wsgi

in wsgi file
First, you need to configure the logging so that it writes to the file and you can see the output. Then you need to specify the paths for your python executable and the web app directory before importing your Flask app instance.

  
> cd /etc/apache2/sites-available

> sudo cp 000-default.conf yoursite.conf

> cd /var/www/html/yoursite

> sudo touch yoursite.log

Database:
-Sqlite connects to database.db

Models used in the project:
-Student:
  registration_number
  name
  age
  course
  password
  
-Course:
  courses
  
The models can be expanded by including more attributes and used as per future requirements

