from typing import List, Any
import requests
from pydantic import BaseModel, Field, ValidationError
import duckdb

# Constants
POSTS_URL = "https://jsonplaceholder.typicode.com/posts"
USERS_URL = "https://jsonplaceholder.typicode.com/users"
DUCKDB_FILE = "posts_users.duckdb"

# Step 1: Define Pydantic Models for Validation
class Post(BaseModel):
    userId: int
    id: int
    title: str
    body: str


class User(BaseModel):
    id: int
    name: str
    username: str
    email: str


# Step 2: Fetch and Validate Data
def fetch_data(url: str) -> List[Any]:
    """Fetch data from a given URL."""
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request is successful
    return response.json()


def validate_data(data: List[Any], model: BaseModel) -> List[Any]:
    """Validate data using a Pydantic model."""
    try:
        return [model(**item).model_dump() for item in data]  # Use model_dump() for Pydantic v2 compatibility
    except ValidationError as e:
        raise ValueError(f"Data validation failed: {e}")


# Step 3: Store Data in DuckDB
def sanitize_string(value: str) -> str:
    """Sanitize a string for SQL insertion."""
    return value.replace("'", "''")  # Escape single quotes


def store_in_duckdb(posts: List[dict], users: List[dict], duckdb_file: str) -> None:
    """
    Store posts and users data into DuckDB tables.
    """
    conn = duckdb.connect(database=duckdb_file, read_only=False)

    # Create and populate posts table
    conn.execute("CREATE OR REPLACE TABLE posts (userId INT, id INT, title STRING, body STRING)")
    for post in posts:
        conn.execute(
            "INSERT INTO posts VALUES (?, ?, ?, ?)",
            (post['userId'], post['id'], sanitize_string(post['title']), sanitize_string(post['body']))
        )

    # Create and populate users table
    conn.execute("CREATE OR REPLACE TABLE users (id INT, name STRING, username STRING, email STRING)")
    for user in users:
        conn.execute(
            "INSERT INTO users VALUES (?, ?, ?, ?)",
            (user['id'], sanitize_string(user['name']), sanitize_string(user['username']), sanitize_string(user['email']))
        )

    print(f"Data successfully stored in DuckDB file at: {duckdb_file}")
    conn.close()


# Step 4: Query Data from DuckDB
def query_duckdb(duckdb_file: str) -> None:
    """
    Query the DuckDB tables to answer specific questions.
    """
    conn = duckdb.connect(database=duckdb_file, read_only=True)

    # Query 1: Number of posts per user
    print("Number of posts per user:")
    print(
        conn.execute("""
            SELECT users.name, COUNT(posts.id) AS post_count
            FROM posts
            JOIN users ON posts.userId = users.id
            GROUP BY users.name
            ORDER BY post_count DESC
        """).fetchdf()
    )

    # Query 2: User with the longest post
    print("\nUser with the longest post:")
    print(
        conn.execute("""
            SELECT users.name, LENGTH(posts.body) AS body_length
            FROM posts
            JOIN users ON posts.userId = users.id
            ORDER BY body_length DESC
            LIMIT 1
        """).fetchdf()
    )

    # Query 3: Top 3 users by total content length
    print("\nTop 3 users by total content length:")
    print(
        conn.execute("""
            SELECT 
                u.name AS user_name,
                SUM(LENGTH(p.body)) AS total_content_length
            FROM posts p
            JOIN users u
            ON p.userId = u.id
            GROUP BY u.name
            ORDER BY total_content_length DESC
            LIMIT 3
        """).fetchdf()
    )

    conn.close()


# Main Execution
def main() -> None:
    """Main execution function."""
    # Fetch data
    posts_data = fetch_data(POSTS_URL)
    users_data = fetch_data(USERS_URL)

    # Validate data
    posts = validate_data(posts_data, Post)
    users = validate_data(users_data, User)

    # Store data in DuckDB
    store_in_duckdb(posts, users, DUCKDB_FILE)

    # Query data in DuckDB
    query_duckdb(DUCKDB_FILE)


if __name__ == "__main__":
    main()