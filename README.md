#1. Solution description:

* The data_getter.py gathers data from Wikipedia about every day of the calendar. At every 2 hours the script scraps data from the pages (ex. March_13, March_14...) and processes it into strings that are split by 'year', 'day', and 'information'. After that the database is checked if there is any entry with the same year, day and information and if so updates it, otherwise it inserts it.

* webserver.py is a webserver made in Flask that receives requests from the user as (http://localhost:5000/?year=2009&category=deaths&day=March_14). The user can also query for a single variable like (http://localhost:5000/?year=2009).

* The whole solution is put into a docker container so it runs the same on  any environment that is tested.

#2. Running instructions:

* For running the solution you need to install the latest version of docker and docker-compose. You also need git for cloning the repo.

```
  $ git clone https://github.com/vladimiriacob/hootsuitehomework
```
```  
  $ cd hootsuitehomework && docker-compose up
```
* The scrapper is not very fast. It needs around 1-2 seconds to scrap the data from one page.
After a couple of minutes go to your localhost:5000 and start making requests to the webserver.
