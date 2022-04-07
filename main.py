from website import create_app

#membuat app
app = create_app()

#nama app
if __name__ == '__main__':
    #menu debug
    app.run(debug=True)
