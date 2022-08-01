# New buildings in Lviv
#### Video Demo:  <https://www.youtube.com/watch?v=fWVZXSSwMNg>
#### Description:
For the final project, I decided to develop a website with ads for the sale of real estate in new buildings in the city of Lviv. On this site, the user can view houses, and developers can add their buildings.

The main users of this website are potential buyers, developers and an administrator.


Visitors can:
- view houses
- use the "Search" button to filter houses by city district, number of rooms in the apartment, availability of parking or commercial premises, number of floors in the building


The "Add an ad" button is intended for developers. In order to add houses, they need to create an account and log in. After registering, developers can:
- edit company data
- edit data about houses, or hide them from being displayed on the website
- add new houses


Administrators can:
- view the list of developers and their houses
- contact developers
- hide the houses from being displayed on the main page

During development, I used the following technologies: Python (Flask, SQLite3, Datetime, OS), HTML, CSS, JavaScript. When developing the frontend part, I set myself the goal not to use pre-written libraries in order to better learn the relationship between HTML and CSS. Unfortunately, due to lack of time, I was unable to develop the functioning of some elements (administrator and developer pages). To view the page of the developer, you need to click "Add an ad" and then "Log in". In the "Developer" field, you need to enter the name of the company (the third line in the ad) and any password (I didn't have time to develop the password check, although I planned this field in the database). To log in as an administrator, add “/admin” to the URL of the main page. ***There is an archive 'developers_database.zip' in the folder 'static'. You need to unzip it so that the path looks like this 'static/developers_database/ + 8 folders inside'.***

I would like to say thank you to everyone who put in their efforts and time to develop and take this course, and also provided an opportunity to take this course for free!
