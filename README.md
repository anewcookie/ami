# ami

OVERVIEW:
This website serves to digitalize AMI inspections. It consists of the following functions:
•	Use a digital checklist to check off a room
•	Store inspections in a database
•	View a company summary of what rooms have been inspected so far each day
•	View any rooms AMI history in detail

ARCHITECTURE:

- ami
    - __pycache__ : folder includes auto generated files
        - ...
    - migrations : includes auto generated files used to migrate the database architecture
        - ...
    - templates
        - ami
            - core.html : includes the sidebar and other global html used by all the other templates
            - inspection.html : the page used to submit room inspections
            - overview.html : the home/landing page for the website
            - room.html : the page used to view the inspection history of a room
            - settings.html : the page used to change a user's profile information
            - signup.html : the page used to sign up for an account
            - summary.html : the page used to see the status of all rooms in the company 
    - __init.py : auto-generated file
    - admin.py : imports models into the admin page.
    - apps.py : defines the ami application class
    - forms.py : the forms used by the website
    - models.py : the database architecture
    - tests.py : includes all the testcases used to test the website
    - urls.py : routes url patterns to specific views
    - views.py : retrieves data and forward it to a specific template
    
- mysite
    - __pycache__ : folder includes auto generated files
        - ...
    - __init__.py : auto-generated file
    - settings.py : includes all of the site settings
    - urls.py : This file is used to route URLs to views.
    - wsgi.py : Includes the WSGI config
    
- static
    - admin : this folder houses the static files for the admin portion of the website
        - ...
    - ami : this folder houses the static files for the user interface portion of the website
        - images : this folder houses the images used on the website
            - academy.jpg : this image is the backround image for the home page
            - cadet.png : this is used as the user image in the top left corner of the website
        - style.css : this is the master css file that all the ami templates reference
- staticfiles : the static files are consolodated to this folder during the deployment of the website
- templates
    - registration : this folder houses the templates for the registration portion of the website.
        - logged_out.html : page which shows after a user has logged out
        - login.html : the login page
        - password_reset_complete.html : page shown after user has successfuly submitted and confirmed their password reset request
        - password_reset_confirmation.html : this page allows the user to input their new password for a password reset
        - password_reset_done.htmml : page shown after user has submitted a password reset request, asking them to check their email to confirm
        - password_reset_form.html : this page allows the user to request a password reset by entering their email
        
TESTING


KNOWN ISSUES
1. There is no way for users to delete inspections. The only way currently is through the admin page

RECOMMENDED IMPROVEMENTS
1. The "Subordinates" page was never implemented. The idea behind this was to allow cadets to quickly view their subordinates AMI status and history. This could be implemented using  the already implemented Position and Inspection models.

2. It would not take much to adapt the Inspection model to support a SAMI inspection

3. Adding functionality to allow authorized cadets to delete inspecitons would be very useful.

4. Instead of just an image for the home page, it could show information that would be useful at a glance. Perhaps important status updates about the user's room and/or company.


LINKS TO REDEPLOY APPLICATION
https://dashboard.heroku.com/apps/cadet-ami/deploy/heroku-git




