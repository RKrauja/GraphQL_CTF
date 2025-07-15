import strawberry
from strawberry.fastapi import GraphQLRouter
import psycopg
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os

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


def connect_to_db():
    return psycopg.connect(**DB_CONFIG)

def validate_session(session_token: str) -> bool:
    return session_token == "Admin token"

def fetch_user_by_id( UserId: int) -> UserType:
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