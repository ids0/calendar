from flaskcalendar import create_app
application = app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
