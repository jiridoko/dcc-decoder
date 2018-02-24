#!/usr/bin/env python3
import yaml

with open("test.yaml", 'r') as s:
    try:
        print(yaml.load(s))
    except yaml.YAMLError as exception:
        print(exception)
