
DotCloud ServiceConfig
======================

What is it?
-----------

DotCloud ServiceConfig is a simple python module to help
different (python-based) dotcloud services find each other
without manually wrangling DSNs, passwords and so on.

How does it work?
-----------------

It's really simple. First you put serviceconfig in your
dotcloud source tree. Then, just before you push your code,
you can run the provided script to create a config file
inside the serviceconfig tree which describes all of the
deployments made for a given application.

At runtime, any Python code can import the module to gain
access to this configuration information.

Detailed Walkthrough
--------------------

For this example, let's say we have a dotcloud app called
"ramen" that has a python-worker deployment called
ramen.worker which will ultimately run Celery and a
RabbitMQ deployment called ramen.rabbitmq.

The celeryd on ramen.worker needs to know how to connect
to RabbitMQ and what credentials to use.

### Generating the config (on your local machine)

After you've created these deployments with the dotcloud
CLI tool, you can run the tool included inside the serviceconfig
distribution to generate the config file:

    bin/dotcloud_serviceconfig_build ramen

This tool uses the dotcloud CLI tool (the "info" subcommand)
to retrieve the list of deployments for ramen and then to retrieve
the configuration for each. It then writes the result into a file
called `config.yaml` alongside the module source file, where
the module can find it at runtime.

You should then arrange for the serviceconfig module and config
file to be pushed as part of your codebase. I achieve this
just by copying it into the root of my project and referencing
it as a requirement for the worker in `dotcloud_build.yml`.

### Using the config (at runtime, on your instances)

The configuration file for celeryd is a Python module, so it
is able to import and use the serviceconfig module.

Here's an example `celeryconfig.py` referencing the rabbitmq service:

    from dotcloud_serviceconfig import config

    rabbitmq = config.rabbitmq
    amqp = rabbitmq.ports.amqp

    BROKER_HOST = amqp.hostname
    BROKER_PORT = amqp.port
    BROKER_USER = amqp.username
    BROKER_PASSWORD = amqp.password
    CELERY_RESULT_BACKEND = "amqp"
    CELERY_IMPORTS = ("kitchen",)

All of the information necessary to find RabbitMQ is obtained
via the serviceconfig module, so the configuration is centralized
in one place where it can easily be updated when necessary.

This also means you can put `celeryconfig.py` under public version
control without worrying about disclosing your credentials. Just
make sure you never check in the config.yaml file inside the
serviceconfig directory, instead regenerating it automatically
from dotcloud when you need it.

Since django's configuration file is also a Python module, you
can use the same technique to configure django-celery to talk
to RabbitMQ, and to configure django to talk to your database
server.

Design Tradeoffs
----------------

Here are some things you should be aware of if you use this module:

- The configuration returned by `dotcloud info` contains root credentials
  for services, so if you use the information exposed by this module
  you will be connecting to all of your services as root, and the
  root passwords for all of your services will be available in the
  clear in the filesystem of all of your instances.

- Obviously since this thing is a python module it's not so useful
  for situations where you need the config information outside of
  Python land. However, the yaml file is on disk and available
  in a pinch.

- The configuration is exposed on a per-deployment basis, so if you
  have a separate set of services set aside for staging you'll need
  to be careful to ask for the right service name in staging vs.
  production to avoid accidentally connecting to the wrong service.

- serviceconfig expects the configurtion file to be written into
  the same directory as its source file. This means you need to
  have the source file in your source tree in order to have the
  config file in your source tree. In practice, this script is
  pretty small so I'd just copy it inline into each of my projects
  and not worry too much about it.

I'm hoping that DotCloud will make available a more robust service
discovery mechanism to allow nodes to dynamically discover each other
at runtime without pre-push config file generation, but this works
until then.

