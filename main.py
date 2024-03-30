from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def get_main_page():
    """the first page every visitor sees"""
    return "Welcome to haha.ru!"


@app.get("/login")
def get_login_page():
    """page where user enters login and password"""
    return "Login page"
