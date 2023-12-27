# Django Api example: Forecast Google Trends

In this tutorial we show an example implementation of a REST API in Django for a forecasting model.

The related article is available [here](https://medium.com/towards-data-science/forecasting-api-an-example-with-django-and-google-trends-9b55046bd578).

For this example we don't use the shared environment at the root of the repository, but we define a custom one inside this folder.

To get started, run the following snippet:
```bash
# Clone the project
git clone git@github.com:davide-burba/code-collection.git

# Move to the right folder
cd code-collection/examples/api-example-django

# Launch the app.
docker compose up -d

# Apply the migrations.
docker compose exec django ./manage.py migrate

# Interactively create a (super)user for your app.
docker compose exec django ./manage.py createsuperuser 
```
and connect to `localhost:8000/gtrends`!

