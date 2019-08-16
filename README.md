Lucky Call
==========

## Introduction

Example project for a radio contest called LuckyCall. The contest is defined by the following
statements:

> Imagine you are running a radio server and you want to give a prize to your beloved
> followers and decide to do the following contest that will be awarded to a random follower:

> During the day, you are going to say a keyword
> After the keyword, all the followers are going to make a request to the server and say the
> KeyWord and a 3 digit number. This number is going to be added to the current result (stored in
> the server). 

> The client which adds a number where the result is multiple of 11 is going to win the prize the
> expect is expected to have a lot of clients making requests to you. If the system fails, it
> should be able to recover how many request you registered before the failure and the current
> results.

## Requirements

* docker
* docker-compose
* Tox (if you want to test the code)

## Usage

To run this application you will need docker-compose, so execute (ideally inside a virtual 
environment):

```bash
$ pip install docker-compose
```

Then, we have to build the existing code to get it working:

```bash
$ docker-compose build
```

Now, everything is ready to be executed. For starting the application, just execute, in a shell:

```bash
$ docker-compose up  # it could be started in background with -d option
```

NOTE: this app is exposing the port 80 as the entrypoint for all expected requests, so in case
you are using this port for other purposes you could either stop it for a while or change the
defined port in docker-compose.yml file to a different (and unused) port.

Then, all internal configuration should have been prepared, as creating the needed database tables
and other needed stuff. You should see some log from the running containers and they will stop at
some point (probably after running database migrations). At this point the application should be
ready to accept our radio requests.

You can test it with:

```bash
$ curl --header "Content-Type: application/json" http://localhost/ -d "{\"user_email\": \"user17395@example.com\", \"keyword\": \"wrong_keyword\", \"number\": 874}"
```

## Contest example

Once you have the application running (see previous section), we'll create a new contest and
we'll make some request as an example of the behaviour.

### Start the contest

To start a new contest with the keyword *beetlejuice*, just run (inside your virtual environment):

```bash
$ docker-compose exec app01 python3 manage.py start_new_contest beetlejuice
```

### Make some requests to the contest

You could now start making your own requests as in the previous chapter; however, in order to ease
the fake requests execution, an script has been created which lets you generated a determined
number of requests for a given keyword. For example, if you want 50 requests for the
keyword *beetlejuice*, you can just use:

```bash
$ ./scripts/generate_sample_requests.py 50 beetlejuice
```

This will output the generated random requests, with some of them invalid (with a number with less
than 3 digits) or incorrect (some of them will use incorrect keywords) to simulate the whole full
experience.

If you really want to run a similar request batch, you can achieve it with:

```bash
$ ./scripts/generate_sample_requests.py 50 beetlejuice | sh
```

Note that by running this you will see in you application logging the incoming requests and how
the load balancer (nginx) is round-robin the requests between your application (in this example
we have two apps in different containers).

### Check the winner

You can check at any moment if there is a winner for the last contest with:

```bash
$ docker-compose exec app01 python3 manage.py check_winner
```

Hopefully there will be a winner; otherwise, you could make more requests and run this command
again until you get the contest's winner.

### Start a second contest

To start a second contest once you have winner (or maybe not, will depend on the luck and on the
received request) just repeat the command for the first section of this chapter and new requests
will be linked to this new contest.

### Stopping thee application

In order to stop the application, use:
* CTRL + C in the shell if you run the app without -d option
* (with -d) Go to a shell and (inside your virtualenv) execute: $ docker-compose stop

Once your application has been stopped, you can delete the containers with the command:

```bash
$ docker-compose rm -f
```

## Testing

For running test, just execute (ideally inside a virtual environment):

```bash
$ pip install tox  
$ tox
```

You should get your tests and syntax results, along with the code coverage.
