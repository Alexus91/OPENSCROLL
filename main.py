from webapp import create_app

# Create the Flask application using the create_app function
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
