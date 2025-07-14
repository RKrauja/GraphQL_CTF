# from flask import *
import strawberry
from strawberry.fastapi import GraphQLRouter
import psycopg
from fastapi import FastAPI


conn = psycopg.connect("dbname=graphql_db user=user password=password host=db port=5432")
curr = conn.cursor()

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
            raise Exception(status_code=405, detail="Invalid session token")
        return fetch_user_by_id(UserId)
    
    @strawberry.field
    def get_Post( PostId: int) -> PostType:
        return fetch_post_by_id(PostId)



def validate_session(session_token: str) -> bool:
    return session_token == "Admin token"

def fetch_user_by_id( UserId: int) -> UserType:
    curr.execute("SELECT NAME, PASSWORD FROM users WHERE id = %s", (UserId,))
    user = curr.fetchone()
    if user is None:
        raise Exception(status_code=404, detail="User not found")
    return UserType(id=UserId, name=user[0], password=user[1])

def fetch_post_by_id(PostId: int) -> PostType:
    curr.execute("SELECT TITLE, CONTENT, AUTHOR_ID FROM posts WHERE id = %s", (PostId,))
    post = curr.fetchone()
    if post is None:
        raise Exception(status_code=404, detail="Post not found")
    author = fetch_author_by_id(post[2])
    return PostType(id=PostId, title=post[0], content=post[1], author=author)

def fetch_author_by_id(author_id: int) -> UserType:
    curr.execute("SELECT NAME, PASSWORD FROM users WHERE id = %s", (author_id,))
    user = curr.fetchone()
    if user is None:
        raise Exception(status_code=404, detail="Author not found")
    return UserType(id=author_id, name=user[0], password=user[1])
    
    
schema = strawberry.Schema(query=Query)

# app = Flask(__name__)

graph_QL_app = GraphQLRouter(schema)

app = FastAPI()

app.include_router(graph_QL_app, prefix="/graphql")

# if __name__ == "__main__":
#     app.run(debug=True, host='0.0.0.0', port=8080)