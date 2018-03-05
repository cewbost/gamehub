Documentation
-------------

The backend uses Sphinx for documentation. To generate the documenation files, go into
the 'doc' directory and run 'make html'. The produced documentation can be found in
'doc/build/html/index.html'.


Project Plan
------------

**1. Team**


Laxmi Thebe
Filippo Vimini
Carl Bostrom



**2. Goal**

In this project, we will create a simple but functional website that allows to play and sell games. Developer will be able to link their games into the website and set a price for the sell. Gamers will be able to buy the games and play directly in the website. The Website will create a game library for each user and collects some basic statistics about the games.  

**3. Plans**

The backend will be implemented using Django. We will begin by setting up a logging system and a documentation system using Sphinx, to aid development. Thereafter the management and authentication of user accounts. The payment system will be replaced with a simple on server toggle while the core functionality is implemented. The tests and the security will be implemented while proper fnctionalities are created.

We will use jQuery and Bootstrap to make the UI responsive and mobile friendly. We will begin working on design right from the start, with continuous testing to ensure that it works on mobile. Unit testing for the frontend scripts will be done using AVA.

**3.1 Models**

![Alt text](doc/wds_readme_pic01.jpg "Db model")

**ER-Diagram**
![Alt text](doc/er_diagram.png "ER diagram for models")

The diagram is more about the concept and actual representation of the relationship than exact definition of attributes.

**3.2 Views**

* Home (/)
  The home view will present the players with a splash screen, and options for signing up, signing in, searching for games, and if the user is logged in, presents the user with her game catalogue.
* Signup (/signup)
  The signup screen.
* Login (/login)
  The login screen.
* Search (/search)
  This view presents the user with the results of a search query. The query itself is passed as a GET parameter. Clicking on a game should redirect the user to the BuyGame view.
* BuyGame (/buy)
  This view gives the player a presentation/description of the game, and asks the player to buy it.
* UploadGame (/upload)
  Developers go through this view to upload a game.
* PlayGame (/play)
  Here the playing takes place.
* ConfirmPayment (/confirm)
  Paying for a game will be done from the BuyGame view. This view implements the backend part of the payment flow.

**3.3 Extra features**

After the basic functionality is implemented, we will implement the following extra features depending on what time permits. These are ranked by priority.

* Better search functionality. A tag system would be helpful.
* Social media sharing.
* REST API. Using django rest\_framework this should not be difficult. This will allow for getting statistics about players, developers and games straight from the database.
* Recommendation system. This one might be difficult to implement, we'll see.

**4. Process and Time Schedule**

We communicate using the messagging application Slack. Most work will be done remotely due to divergent schedules of teammates. To ensure code quality will will require that feature branches are merged not by the developer behind the feature. This will work as a simple code review process.

* 25.12-30.12:
  Development begins. We set up logging and documentation system and begin working on the backend, starting with authentication.
* 1.1-21.1:
  We begin work on the frontend design, with continuous testing on phone. Most core features should be implemented during this time.
* 28.1-5.2:
  Polish for the frontend. The payment system should be implemented this week. If time permits we begin implementing tag system here.
* 5.2-20.2:
  Assuming everything else works we use this time to implement extra features, and test the final product.

**5. Testing**

The backend will have tests for all views and all response cases. For the frontend we will use AVA. To ensure code quality we require all features must have unit tests before merging to master.

The testing of the frontend will be done continuously during development, both on desktop and phone. During the last week we will do a final test of the apps security.

**6. Risk Analysis**

**7. Final Submission**

## Features implemented **[Feature (points)] => description**
Let's describe the feature in more details :)
1. Authentication (200) => We implemented authentication using Django Auth - and
  email validation is required before the account is activated. We used SMTP for
  deployment whereas console for the test purpose. Third party login is developed
  and it currently works with Google - the only downfall of the solution at the
  moment is it keeps on asking to update either a user is a developer or a player
  which implies that a user can be both player and developer if he chooses once
  player and next developer (Many-To-Many between User Group relationship)
2. Basic Player Functionalities (300) => Basic player functionalities are
  implemented well - a user can play the game and save the state of the game or
  load the game. A game is only available for play once you purchase the game.
3. Basic Developer Functionalities (200) => A developer can upload a game - and
  he can play his own game as well.
4. Game/service interaction (200) => GameService interaction is fully implmeneted
  to our understanding. A user has to save the state manually though (when a user
  closes the browser tab, it does not  automatically save for example)
5. Quality of Work (90)
6. Non-functional requirements (175)
7. Save/load and resolution feature (100)
8. 3rd party login (100)
9. RESTful API (70)
10. Own Game (0)
11. Mobile Friendly(50)
12. Social Media Sharing (40) - Social Media sharing works and the detail of the
  games are posted as well.

## 3 Task Division
Task division was more about communication than planning after we decided how to
approach in the beginning. We used Slack for the communication. And discussed
our issue in the slack. For example, we proposed like - hey, I am now going to
implement this feature - and the person would be responsible for that feature.
There were some aspects we were more focused definitely as we found it easier to
proceed that way due to the difference on in what phase of the project we can
commit. For example, Filippo was traveling in the beginning of our start while
two other of us were on holiday and thought of spending on doing something. But,
still we managed to get ourselves involved in all technology stacks.
Was there any difficulties?
As a team, probably not really - because we were supporting each other and
communicating well. What one could not handle, could have been handled by another
member. But, personally, I think we had some problems though.
Who did what?
Laxmi implemented the user accounts registering/login/logout, authentication, most
of the models, and the interaction between the site and the games. Filippo worked
mostly on frontend, making it responsive and mobile friendly, and managing the
uploading of images. Carl set up the logging system, documentation system,
implemented the search functionality, uploading of games and the rest api.

