from myproject import create_app


app = create_app()


# cd ~/venvs/myproject/bin
# . activate
# cd ~/projects/myproject
# export FLASK_APP=myproject
# export FLASK_ENV=development
# export APP_CONFIG_FILE=/home/ec2-user/projects/myproject/myproject/config/development.py
# flask run -h 0.0.0.0
if __name__ == "__main__":
    app.run()
