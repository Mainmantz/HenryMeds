# Reservation - Backend v3

## Prerequisites
- Running on a mac :) (trade off)
- Install homebrew  https://brew.sh/
- (Optional) Install TablePlus if you want to have a nice view of your data https://tableplus.com/

```
brew install postgres@15
```

Make sure postgres had been added to PATH, brew will give suggestions on how to do this

```
brew services start postgresql@15
createdb henrydb
```

To run postgres without using a background service so you can see the logs. Run this (below) instead of `brew services start postgresql@15`

```
LC_ALL="C" /usr/local/opt/postgresql@15/bin/postgres -D /usr/local/var/postgresql@15
```


## Running the app locally
```
python3.11 -m venv venv
. venv/bin/activate
python3.11 -m pip install -r requirements.txt
python3.11 -m uvicorn main:app --reload
```

## Tests

```
pytest tests/tests.py
```

## Evaluation

This will be evaluated similar to a real-world submission, including:

1. **Does the code solve the business problem?**
* It does! With the four newly defined endpoints, providers are able to define their availability and clients are able to fill that availability without overlapping and allowing clients to rebook stale reservations

2. **What trade-offs were made, how wise are they?**
* One trade off for timing was a very limited database design, for example, not having defined providers or clients, we are assuming whoever is calling the endpoint already has some setup. Therefore, we are just using the name of each to keep state. 

* Not containerizing this for production, only setup to run locally, with more time, would create a DockerFile to make this easily deployable across any system. 

* Not using UTC time, this does use local time

* Updating expired reservations every 15 minutes, would have to monitor user activity to overall see how well this would operate. Do we see a lot of not confirmed reservations? Is this a short enough cadence to allow good opportunities to fill appointments? Should the GET appointments call run this prior to returning results? 

* Allow deletes but ran out of time / not a requirement

* I had the debate between adding another column to slots to say whether or not its reserved but ultimately decided to do this via joins. I believe that helps with data redundancy so we are not keeping track of two "confirmed" fields but does introduce a join which could effect performance. Overall in this case, data consistency is more important than speed. 

* Would also want to add some additional edge cases, for example, in theory could book two appointments during the same timeframe if two different providers had a slot open.

* MORE TESTS but with timing, at least wanted to get the usual fastapi scaffolding in place to showcase. Another testing techinque we could use is creating abstractmethod functions to help us mock up our API. 

* Most of these decisions were because of time, in a production system we would love to see every one of these, so not wise overall but wise because of time constraints 

3. **How clean/well structured is the code?**
* Follows basic python fastapi standards, would love to continue seperating lines of business out further if I had more time. Some additional improvements could also be type hints, further seperarting each model out into its our file, etc. 

4. **What ‘extra’ factors are there, that show exceptional talent?**
* Setup local postgres henrydb to store everything instead of using a quicker API state. Showcasing more advanced Fastapi features, postman env for ease of test, error handling, and testing. Also uses an ORM approach rather than building up sql strings. 
