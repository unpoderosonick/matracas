### Create virtual env
python3 -m venv myenv

### install dependencies

cd app
pip install -r requirements.txt

note: be aware if there are a deprecated dependecy as postgress

### VS tools:
configure the "format on save" using this tutorial https://marcobelo.medium.com/setting-up-python-black-on-visual-studio-code-5318eba4cd00

### Please docker works
configure docker
https://medium.com/analytics-vidhya/django-with-docker-and-docker-compose-python-part-2-8415976470cc


### fly.io commands:

https://fig.io/manual/fly

flyctl deploy
flyctl secrets list/set
flyctl apps restart bold-snowflake-842  // after set a var env, restart is enough instead of deploy
flyctl ssh console --app bold-snowflake-842-db
flyctl postgres connect --app bold-snowflake-842-db

### Secret Values
The secret env vars values are in bichocj > google drive > secrets > app
