from myproject import create_app


app = create_app()


# export FLASK_APP=myproject
# export FLASK_ENV=development
# flask run
if __name__ == "__main__":
    app.run()
