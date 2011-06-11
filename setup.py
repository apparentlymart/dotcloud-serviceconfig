from setuptools import setup

setup(
    name='dotcloud-serviceconfig',
    version='1.0',
    packages=['dotcloud_serviceconfig'],
    include_package_data=True,
    data_files=[['dotcloud_serviceconfig', ['dotcloud_serviceconfig/config.yaml']]],

    requires=['PyYAML'],
)
