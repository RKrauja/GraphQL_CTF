import strawberry
from strawberry.fastapi import GraphQLRouter
import psycopg
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from dotenv import load_dotenv
import os
import secrets
from datetime import datetime, timedelta

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"), 
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

app = FastAPI()

@strawberry.type
class UserType:
    id: int
    name: str
    password: str

@strawberry.type
class PostType:
    id: int
    title: str                          
    content: str
    author: UserType

@strawberry.type
class Query:
    @strawberry.field
    def get_User( UserId: int, session_token: str) -> UserType:
        if not validate_session(session_token):
            raise Exception("Invalid session token")
        return fetch_user_by_id(UserId)
    
    @strawberry.field
    def get_Post( PostId: int) -> PostType:
        return fetch_post_by_id(PostId)
    
    @strawberry.field
    def get_all_posts() -> list[PostType]:
        return fetch_all_posts()
    
    @strawberry.field
    def get_users_posts(UserId: int) -> list[PostType]:
        with connect_to_db() as conn:
            with conn.cursor() as curr:
                curr.execute("SELECT id FROM posts WHERE author_id = %s", (UserId,))
                post_ids = curr.fetchall()
        if not post_ids:
            raise Exception("No posts found for this user")
        posts = []
        for post_id in post_ids:
            posts.append(fetch_post_by_id(post_id[0]))
        return posts
    

def connect_to_db():
    return psycopg.connect(**DB_CONFIG)
        
def fetch_user_by_id(UserId: int) -> UserType:
    with connect_to_db() as conn:
        with conn.cursor() as curr:
            curr.execute("SELECT NAME, PASSWORD FROM users WHERE id = %s", (UserId,))
            user = curr.fetchone()
    if user is None:
        raise Exception("User not found")
    return UserType(id=UserId, name=user[0], password=user[1])

def fetch_post_by_id(PostId: int) -> PostType:
    with connect_to_db() as conn:
        with conn.cursor() as curr:
            curr.execute("SELECT TITLE, CONTENT, AUTHOR_ID FROM posts WHERE id = %s", (PostId,))
            post = curr.fetchone()
    if post is None:
        raise Exception("Post not found")
    author = fetch_author_by_id(post[2])
    return PostType(id=PostId, title=post[0], content=post[1], author=author)

def fetch_author_by_id(author_id: int) -> UserType:
    with connect_to_db() as conn:
        with conn.cursor() as curr:
            curr.execute("SELECT NAME, PASSWORD FROM users WHERE id = %s", (author_id,))
            user = curr.fetchone()
    if user is None:
        raise Exception("Author not found")
    return UserType(id=author_id, name=user[0], password=user[1])

def fetch_all_posts() -> list[PostType]:
    with connect_to_db() as conn:
        with conn.cursor() as curr:
            curr.execute("SELECT id, TITLE, CONTENT, AUTHOR_ID FROM posts")
            posts = curr.fetchall()
    post_list = []
    for post in posts:
        author = fetch_author_by_id(post[3])
        post_list.append(PostType(id=post[0], title=post[1], content=post[2], author=author))
    return post_list
    
schema = strawberry.Schema(query=Query)
graph_QL_app = GraphQLRouter(schema)
app.include_router(graph_QL_app, prefix="/graphql")





@app.get("/")
def homepage():
    return FileResponse("templates/index.html")

@app.get("/post")
def post_detail(post_id: int):
    return FileResponse("templates/post_detail.html")

@app.get("/login")
def login_page():
    return FileResponse("templates/login.html")

@app.post("/login")
def login(request: dict):
    username = request.get("username")
    password = request.get("password")
    
    user = authenticate_user(username, password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    session_token = create_session(user.id)
    
    response = JSONResponse({"user_id": user.id, "message": "Login successful"})
    response.set_cookie(key="session_token", value=session_token, httponly=True)
    return response

@app.post("/logout")
def logout(request: Request):
    session_token = request.cookies.get("session_token")
    if session_token:
        destroy_session(session_token)
    
    response = JSONResponse({"message": "Logged out successfully"})
    response.delete_cookie("session_token")
    return response

@app.get("/profile")
def profile(request: Request):
    session_token = request.cookies.get("session_token")
    
    if not session_token or not validate_session(session_token):
        return RedirectResponse(url="/login", status_code=302)
     
    return FileResponse("templates/profile.html")

@app.get("/register")
def register_page():
    return FileResponse("templates/register.html")

@app.post("/register")
def register(request: dict):
    username = request.get("username")
    password = request.get("password")
    confirm_password = request.get("confirm_password")
    
    # Basic validation
    if not username or not password or not confirm_password:
        raise HTTPException(status_code=400, detail="All fields are required")
    
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    
    # Check if user already exists
    if user_exists(username):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Create new user
    user_id = create_user(username, password)
    
    # Create session for the new user
    session_token = create_session(user_id)
    
    response = JSONResponse({"user_id": user_id, "message": "Registration successful"})
    response.set_cookie(key="session_token", value=session_token, httponly=True)
    return response

def user_exists(username: str) -> bool:
    with connect_to_db() as conn:
        with conn.cursor() as curr:
            curr.execute("SELECT id FROM users WHERE name = %s", (username,))
            return curr.fetchone() is not None

def create_user(username: str, password: str) -> int:
    with connect_to_db() as conn:
        with conn.cursor() as curr:
            curr.execute(
                "INSERT INTO users (name, password) VALUES (%s, %s) RETURNING id",
                (username, password)
            )
            user_id = curr.fetchone()[0]
            conn.commit()
    return user_id

def authenticate_user(username: str, password: str):
    with connect_to_db() as conn:
        with conn.cursor() as curr:
            curr.execute("SELECT id, name, password FROM users WHERE name = %s AND password = %s", (username, password))
            user = curr.fetchone()
    if user is None:
        return None
    return UserType(id=user[0], name=user[1], password=user[2])

def create_session(user_id: int) -> str:
    session_token = secrets.token_urlsafe(32)
    expires_at = datetime.now() + timedelta(hours=24) 
    
    with connect_to_db() as conn:
        with conn.cursor() as curr:
            curr.execute(
                "INSERT INTO sessions (token, user_id, expires_at) VALUES (%s, %s, %s)",
                (session_token, user_id, expires_at)
            )
            conn.commit()
    
    return session_token

def validate_session(session_token: str) -> bool:
    with connect_to_db() as conn:
        with conn.cursor() as curr:
            curr.execute(
                "SELECT user_id, expires_at FROM sessions WHERE token = %s",
                (session_token,)
            )
            session = curr.fetchone()
    
    if session is None:
        return False
    
    # Check if session has expired
    if datetime.now() > session[1]:
        # Clean up expired session
        destroy_session(session_token)
        return False
    
    return True

def get_user_from_session(session_token: str) -> int:
    with connect_to_db() as conn:
        with conn.cursor() as curr:
            curr.execute(
                "SELECT user_id FROM sessions WHERE token = %s AND expires_at > %s",
                (session_token, datetime.now())
            )
            result = curr.fetchone()
    
    return result[0] if result else None

def destroy_session(session_token: str):
    with connect_to_db() as conn:
        with conn.cursor() as curr:
            curr.execute("DELETE FROM sessions WHERE token = %s", (session_token,))
            conn.commit()

@app.get("/api/current-user")
def get_current_user(request: Request):
    session_token = request.cookies.get("session_token")
    
    if not session_token or not validate_session(session_token):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user_id = get_user_from_session(session_token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid session")
    
    user = fetch_user_by_id(user_id)
    return {"id": user.id, "name": user.name}
