#!/bin/bash
cd ~/projects/myproject
export FLASK_APP=myproject
export FLASK_ENV=development
export APP_CONFIG_FILE=/home/ec2-user/projects/myproject/myproject/config/development.py
. ~/venvs/myproject/bin/activate
