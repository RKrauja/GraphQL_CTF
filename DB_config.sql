-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    token VARCHAR(255) UNIQUE NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id),
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sessions_token ON sessions(token);
CREATE INDEX idx_sessions_expires ON sessions(expires_at);

-- Create posts table
CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Insert sample data
INSERT INTO users (name, password) VALUES 
    ('John Doe', 'secret'),
    ('Jane Smith', 'password123'),
    ('Bob Johnson', 'mypassword');

INSERT INTO posts (title, content, author_id) VALUES 
    ('First Post', 'This is my first blog post about GraphQL.', 1),
    ('Learning GraphQL', 'GraphQL is a powerful query language for APIs.', 1),
    ('Database Design', 'Proper database design is crucial for scalability.', 2),
    ('Flask and GraphQL', 'Combining Flask with GraphQL creates powerful APIs.', 3);