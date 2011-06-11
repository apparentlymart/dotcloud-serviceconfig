
import yaml
import os
import datetime
import urlparse


config_file = os.path.dirname(__file__) + "/config.yaml"


config_dict = yaml.load(file(config_file, "r"))


class Config(object):
    _dict = None

    def __init__(self, dict):
        self._dict = dict

    def __getattr__(self, name):
        if name not in self._dict:
            raise AttributeError(name)

        service_dict = self._dict[name]
        return Service(service_dict)


class Service(object):
    _dict = None

    def __init__(self, dict):
        self._dict = dict

    def __getattr__(self, name):
        if name not in self._dict:
            raise AttributeError(name)
        return self._dict[name]

    @property
    def created_at(self):
        ts = self._dict["created_at"]
        return datetime.datetime.utcfromtimestamp(ts)

    @property
    def ports(self):
        ports_list = self._dict["ports"]
        return Ports(ports_list)


class Ports(object):
    _dict = None

    def __init__(self, list):
        self._dict = {}
        for port_dict in list:
            self._dict[port_dict["name"]] = port_dict["url"]

    def __getattr__(self, name):
        if name not in self._dict:
            raise AttributeError(name)
        return Port(self._dict[name])


class Port(object):

    def __init__(self, url):
        parts = urlparse.urlparse(url, "http", True)
        self.url = url
        self.scheme = parts.scheme
        self.netloc = parts.netloc
        self.path = parts.path
        self.params = parts.params
        self.query = parts.query
        self.fragment = parts.fragment
        self.username = parts.username
        self.password = parts.password
        self.hostname = parts.hostname
        self.port = parts.port


config = Config(config_dict)

