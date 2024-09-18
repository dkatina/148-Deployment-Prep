## Learning Objectives

- The students should be able to configure and deploy web services and databases on Render's platform, demonstrating proficiency in setting up cloud-based infrastructures.
- The students should be able to utilize continuous deployment practices with GitHub Actions to automate the deployment process of their applications on Render, enhancing their workflow efficiency.
- The students should be able to demonstrate an understanding of security measures such as SECRETS KEYS and SECRETS VALUES, ensuring the protection of their applications and data on Render's platform.

### Cloud Service Providers

Once you are done building your application you will need to host these apps, and that’s where cloud service providers come into play; these are also known as hosting platforms or cloud platforms, are services that provide the infrastructure and tools necessary to deploy, host, and manage applications or websites on the internet.

Cloud Providers:
- Amazon Web Service (AWS)
- Microsoft Azure
- Google Cloud Platfor (GCP)
- Heroku 
- Render
- Digital Ocean
- Netlify

Today we'll beusing Render as it offers a free teir for both website and database hosting, ease of use, and compatibility with Github actions to allow us to contiue setting up our CI/CD pipeline

#### Adding Tests for CI

```
pip install faker
```

Before we worry about Deploying, we want to set up the CI portion for our flask app. To start we are going to set up some test cases to run on push to github.

In our `Flask-API` we are going to add a `test_customer.py` file. 

Here we will:

- Create a test to test the full functionality of our POST /customers endpoint
- We'll also cover the same endpoint using a `@patch` that prevents it from actually interacting with the database, so are tests don't store data to our db

Once we're done we'll incorporate our github workflow from yesterday and push to github.

### Prep for Deployment

There is ALOT that needs to be done to get our app in deployment shape.

First and foremost we need to: 

```
pip install gunicorn
```
Gunicorn is a python webserver gateway that will be required to build our app on a hosting platform.

With this in place we can remove our `if __name__ == '__main__'` app runner as gunnicorn will run our app for us.

#### Production Config

Now that we are headed for production we need to configure our app for it. Our production config wont be much different from our development, but it will need to be out of debug mode and pointed at a Live database.

#### Hosting a Database

Remeber that our MySQL databases only exist on our computer. When we go to deploy we want the database our API is linked to, to be persistent so we need to host our db.

We can do this on Render:

- Make an account (use your github credentials to do it)
- Click `+ New` in the top right hand corner
- `PostgreSQL` from the drop down
- Give the db a `name`, `user`, and select the free tier (unless you're feelin boujie)
- `Create Database`
- Once the db status is `Available` grab the `External Database URL`
- This is private info so we want to keep it safe in a `.env` file that wont get pushed to github
- using the os package pull the URI from your `.env` and use it in your Production config

```
pip install python-dotenv
```
*make sure this doesn't end up in your requirements.txt*

Because this is a Postgresql DB and not MySQL, we'll need a new adapter as `mysql-connector-python` won't work.

```
pip install psycopg2
```
on **Mac** it's `psycopg2-binary`, you may need `psychopg2` for deployment, but try without first.

Make sure to change it to `app = create_app('ProductionConfig')`


### Deploy

It's time to deploy, back to render we want to:

- Click `+ New`
- `Web Service` from dropdown
- `Public Git Repository`
- Paste in the link to the repo
- Can leave pretty much all the settings as default
- Free Tier
- And add in your SQLALCHEMY_DATABASE_URI environment variable
- `Deploy Web Service` and hope for the best

#### Adjust your Swagger Config 

*this will come after we deploy and have our domain*

Right now swagger is configured to run on localhost.

- change host to new domain
- change scheme to https

#### libpq-dev

pyscopg2 can get confused in some deployment environments and libpq helps iron out some of the kinks so we want to make sure it is involved in our deployment build so add the following step to your `yaml` jobs under `Set up Python`

```
- name: Install libpq-dev
        run: |
          sudo apt-get update
          sudo apt-get install -y libpq-dev
```


### Set Up CD

Right now, whenever we push to that repo the app will automatically re-deploy, even if the tests and build fail, which will mean our "production" app dies. We want to set up an action that will only depoly on successful test and build.

To do this we will need the following:

- service-id: This is the id of our web service and can be found in settings by Deploy Hook, or in service url ex.: `srv-oajkndfg98qj35p98efhghnqe`
- While in service settings turn `Auto-Deploy` to no

- API Key: Can Create One in Profile Pic > Account setting > API Keys
- Take these to your github repo settings > secrets and variables and create repository secrets:

    - RENDER_API_KEY
    - SERVICE_ID

Once we have our service id and secret key set it's time to add the `deploy` job to our `main.yaml` file.

It will be pretty much the same as the `build` job with this additional step

``` bash
- name: Deploy to production
        uses: johnbeynon/render-deploy-action@v0.0.8
        with:
          service-id: ${{ secrets.SERVICE_ID }} 
          api-key: ${{ secrets.RENDER_API_KEY }} 
```


srv-crliee56l47c7383klbg
rnd_NPMgctiR4pV2tKaPLp5twGhYgYlK