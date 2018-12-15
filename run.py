#!/usr/bin/python3

from app import create_app
import os

default_config = ('../default_config.py')
app = create_app(default_config)
