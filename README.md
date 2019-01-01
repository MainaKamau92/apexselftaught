
# Project Title

iReporter Api endpoints

# Project Backstory
Apex is an idea that aims at creating a site that gives self
taught professionals in the fields of design and software
engineering a chance to get hired by firms without any formal
certification. Itis based of the belief that getting a degree,
diploma and the like however important it may be should not
suffice as reason enough to exercise monopoly over said fields
It's an ambitious project, completely open source and a first
in many respects in the region i'm from.

# Prerequisites
For the web application to run locally a few requirements are necessary:
* Python 3 or older
* Virtualenv(python)
* Pip(the python package installer)
* Postgres database admin ( for managing the database)
* All the listed dependencies in the **requirements.txt** file
* Git 
>> NB: All the commands in the README.md on setup and running assume a windows based environment

## Getting Started
1.  Run the following command from your git command line tool

    * `git clone https://github.com/MainaKamau92/apexselftaught.git`

    >> The command clone a local copy of the project folder on your local machine
2. Navigate into the folder that has been created and create a virtual environment and activate it
    * `cd apexselftaught`
    * `virtualenv venv`
    * `venv\Scripts\activate`
3. Make the necessary changes to the postgres configurations for the database to point to your local postgres address this can be done in the config.py file
4. Run the requirements.txt file to install all the required dependencies
    * `pip install -r requirements.txt`
5. Run the migrations command to setup the database tables
    * `flask db init`(this command should create a migrations folder)
    * `flask db migrate`
    * `flask db upgrade`
6. Run the `.bat` file (this file automatically activates the virtual environment, if already activated ignore this file until reactivation is necessitated)
    * `> .bat`
7. Run the `env.bat` batch file that automatically adds your environments(you might need to edit this file to match some of your local paths)
    *`> env.bat`
8. Run the `flask run` command to start the application(it should ideally be served on your local address(`127.0.0.1:5000`) on port 5000)
9. You should get this response on running the application
    ```
    * Serving Flask app "run.py" (lazy loading)
    * Environment: development
    * Debug mode: on
    * Restarting with stat
    * Debugger is active!
    * Debugger PIN: 194-xxx-782
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    ```


### Installing
To install all the dependencies run from the root folder
```
pip install -r requirements.txt
```

### Some of the Working Routes

#### Index/Home route
``localhost:5000/``

![Alt](/app/static/img/Readme/homepage.png "Homepage")

#### Registration Route

```
http://localhost:5000/register/
```
![Alt](/app/static/img/Readme/register.png "Homepage")

#### Login Route

```
http://localhost:5000/login/
```
![Alt](/app/static/img/Readme/login.png "Homepage")


#### Contact Route

```
http://localhost:5000/contact/
```
![Alt](/app/static/img/Readme/contact.png "Homepage")


#### Freelancer profile Route

```
http://localhost:5000/freelancer/dashboard
```
![Alt](/app/static/img/Readme/profile_freelancer.png "Homepage")


#### Employer profile Route

```
http://localhost:5000/employer/dashboard
```
![Alt](/app/static/img/Readme/profile_employer.png "Homepage")


#### Jobs Route

```
http://localhost:5000/jobs
```
![Alt](/app/static/img/Readme/jobs.png "Homepage")

#### Freelancers Route

```
http://localhost:5000/freelancers
```
![Alt](/app/static/img/Readme/freelancers.png "Homepage")




## Working routes summary

	 	
| Route |  Description |
|---|---|
|http://localhost:5000/  | Home/Index Route Directs to the homepage of the app |
|http://localhost:5000/register  | Registration route of the web app  |
|http://localhost:5000/login | Logs in a user that has already been registered  |
|http://localhost:5000/freelancer/dashboard  | From login redirects user to dashboard if they are a freelancer  |
|http://localhost:5000/employer/dashboard  | From login redirects user to dashboard if they are an employer  |
|http://localhost:5000/jobs  | Lists all the available jobs  |
|http://localhost:5000/freelancers  | Lists all available freelancers  |
|http://localhost:5000/freelancer/3/resume/update | Edits an existing freelancer resume  |
|http://localhost:5000/freelancer/projects   | Allows freelancer to add project to his profile  |
|http://localhost:5000/freelancers/13  | View a single freelancer based on their id | 


## Running the tests

In order to run the tests you will require ```nose2``` a python testing tool that can be easily installed by running the command ```pip install nose2```

Then proceed to run the ```nose2 -v --with-coverage``` command from the root directory to get all the results on the test inclusive of the coverage.


## Built With

* [Flask](http://flask.pocoo.org/) - The python web microframework



## Authors

* **Maina Kamau** 


## License

This project is licensed under the MIT License for details see [LICENSE](https://github.com/MainaKamau92/iReporter/blob/master/LICENSE)

