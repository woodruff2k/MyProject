from myproject import create_app


app = create_app()


# cd ~/venvs/myproject/bin
# . activate
# cd ~/projects/myproject
# export FLASK_APP=myproject
# export FLASK_ENV=development
# export APP_CONFIG_FILE=/home/ec2-user/projects/myproject/myproject/config/development.py
# export FLASK_ENV=production
# export APP_CONFIG_FILE=/home/ec2-user/projects/myproject/myproject/config/production.py
# flask run -h 0.0.0.0
# gunicorn --bind 127.0.0.1:5000 "myproject:create_app()"
# gunicorn --bind unix:/tmp/myproject.sock "myproject:create_app()"
if __name__ == "__main__":
    # app.run(debug=True)
    app.run()
