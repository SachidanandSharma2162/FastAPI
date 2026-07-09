from fastapi import FastAPI

app = FastAPI() # Create the FastAPI instance

@app.get("/") # Decorator: defines a GET endpoint at root URL "/"
def hello():
    return {"message": "Hello, World!"} # Auto-converted to JSON

@app.get("/about")
def about():
    return {"message": "This is the about section."}