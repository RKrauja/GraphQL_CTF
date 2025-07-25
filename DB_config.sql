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
    ('Bob Johnson', 'mypassword'),
    ('Alice Williams', 'alicepass'),
    ('Charlie Brown', 'charlie123'),
    ('Emily Clark', 'emilysecure'),
    ('David Martinez', 'davidsafe'),
    ('Sophia Turner', 'sophiapass'),
    ('Michael Lee', 'michaelpw'),
    ('Linda Kim', 'lindakim2025'),
    ('Chris Evans', 'chrisevans321'),
    ('Olivia Harris', 'flag{WASNTTHISASHITSHOW}'), -- Here is the flag lmao
    ('Ethan Wright', 'ethanwright'),
    ('Grace Hall', 'gracehall'),
    ('Ryan King', 'ryanking'),
    ('dolorem','Nesciunt voluptas pariatur quod explicabo quibusdam aut culpa.'),
    ('asperiores','Impedit harum quo quod officia.'),
    ('ut','Blanditiis maxime et deserunt rerum et vero necessitatibus.'),
    ('quo','Pariatur debitis blanditiis enim ut sed iusto.'),
    ('blanditiis','Dolorem quae et quaerat facilis autem qui et.'),
    ('dolore','Fuga recusandae iusto nobis repudiandae molestiae similique nesciunt.'),
    ('amet','Corporis consequatur minus sit ipsam qui.'),
    ('aut','Sit harum praesentium qui cupiditate adipisci in.'),
    ('temporibus','Praesentium eum doloremque et qui.'),
    ('hic','Cum ea incidunt sint commodi perferendis.'),
    ('magni','Voluptatem aut corporis dicta at delectus libero rerum.'),
    ('modi','Fuga praesentium sequi veritatis esse itaque tenetur autem repellendus.'),
    ('est','Et sequi qui iure sapiente dolorem corporis natus quia.'),
    ('error','Quibusdam molestias qui molestiae.'),
    ('vel','Tenetur dolore accusantium sed quia.'),
    ('alias','Atque et inventore et quod reiciendis aut.'),
    ('ea','Reprehenderit nisi voluptas repudiandae quia ab harum.'),
    ('aliquid','Ipsum architecto explicabo repudiandae vero cumque tempora hic eligendi.'),
    ('optio','Doloribus quo aut omnis eaque.'),
    ('excepturi','Earum qui in est reprehenderit reprehenderit in consectetur sit.'),
    ('minima','Minus a labore eum aut velit ut.'),
    ('id','Cupiditate voluptate neque dicta voluptates aliquam.'),
    ('et','Ratione non nostrum voluptatum facilis.'),
    ('tempora','Dolor accusamus voluptas cum nihil.'),
    ('facere','Temporibus animi optio velit cum.'),
    ('molestiae','Explicabo dolore non dicta voluptates officia sed qui.'),
    ('ab','Earum laborum amet voluptas exercitationem illo qui.'),
    ('expedita','Itaque suscipit nulla eligendi labore porro esse sapiente laudantium.'),
    ('illum','Et corrupti sed omnis qui.'),
    ('eos','Et consequatur aliquid nostrum facilis quia.'),
    ('consequatur','Consequatur doloribus quod aliquid a quas officiis.'),
    ('quos','Accusamus molestiae labore nihil cupiditate tenetur et.'),
    ('animi','Animi soluta quod iure sunt.'),
    ('sed','Quod sint maiores eum rerum ab.'),
    ('velit','Possimus et non nesciunt quae ab quia.'),
    ('sit','Enim voluptas eius voluptatem at iure alias iure.'),
    ('earum','Iure dolorem eum at sapiente quis nulla.'),
    ('vitae','Ut quae ipsum molestias quis pariatur.'),
    ('harum','Earum qui dolor temporibus voluptates.'),
    ('quas','Totam ullam unde qui.'),
    ('quis','Est voluptas repellat aperiam sit qui eveniet.'),
    ('similique','Repellat unde et quas.'),
    ('qui','Quaerat quisquam voluptatem asperiores ducimus harum aut eveniet.'),
    ('ipsa','Ut distinctio quod et reiciendis cum eos quia.'),
    ('provident','Ea modi dolorem saepe sit ipsam animi rerum.'),
    ('aperiam','Quia fugit accusantium maiores vitae.'),
    ('nihil','Ipsa quae soluta aut saepe.'),
    ('maxime','Quia ipsum quia exercitationem occaecati.'),
    ('odit','Minus nihil in repudiandae voluptatem quia quisquam.'),
    ('labore','Eos suscipit quasi ipsam nam.'),
    ('dolorum','Incidunt saepe voluptatem deserunt eligendi.'),
    ('quaerat','Dicta eos nisi fuga maxime dolore cupiditate.'),
    ('rerum','Aut perspiciatis et et blanditiis vero illo tenetur.'),
    ('eum','Quis ut error quis officia saepe.'),
    ('maiores','Perferendis consectetur placeat quasi est consequatur et dolorum.'),
    ('nemo','Voluptate omnis provident maiores debitis.'),
    ('dolores','Enim assumenda sed mollitia mollitia quos nesciunt sequi.'),
    ('nesciunt','Dolores ipsa beatae id vitae laboriosam ut et aut.'),
    ('ullam','Doloremque qui sit eum laboriosam.'),
    ('voluptatem','Distinctio laboriosam quos voluptatem.'),
    ('itaque','Nisi quia qui eligendi ea dolores.'),
    ('facilis','Quibusdam repellendus odit veniam at.'),
    ('neque','Dolores aspernatur et maxime.'),
    ('soluta','Minima fugiat vero nostrum sunt occaecati velit voluptatem odit.'),
    ('dolor','Corporis repellat praesentium aut tenetur sunt.'),
    ('pariatur','Hic dolore provident omnis magnam quae animi aut ad.'),
    ('corrupti','Hic magnam dicta ut sed.');

INSERT INTO posts (title, content, author_id) VALUES 
    ('First Post', 'This is my first blog post about GraphQL.', 1),
    ('Learning GraphQL', 'GraphQL is a powerful query language for APIs.', 1),
    ('Database Design', 'Proper database design is crucial for scalability.', 2),
    ('Flask and GraphQL', 'Combining Flask with GraphQL creates powerful APIs.', 3),
    ('PostgreSQL Tips', 'Here are some tips for using PostgreSQL effectively.', 4),
    ('Frontend Frameworks', 'React, Vue, and Angular are popular choices.', 5),
    ('Docker Basics', 'Getting started with Docker containers for development.', 6),
    ('REST vs GraphQL', 'Comparing REST APIs with GraphQL.', 7),
    ('Unit Testing in Python', 'How to write effective unit tests in Python.', 8),
    ('Security Best Practices', 'Protecting your applications from common vulnerabilities.', 9),
    ('Continuous Integration', 'Automating your build and test processes.', 10),
    ('Scaling Web Apps', 'Techniques for scaling web applications.', 11),
    ('Async Programming', 'Understanding asynchronous programming in JavaScript.', 12),
    ('CSS Tricks', 'Some useful CSS tricks for modern web design.', 13),
    ('Microservices', 'Designing applications using microservices architecture.', 14),
    ('Debugging Techniques', 'Effective debugging strategies for developers.', 15),
    ('SQL Joins Explained', 'A simple explanation of SQL joins.', 2),
    ('Serverless Functions', 'Introduction to serverless computing.', 5),
    ('API Authentication', 'Methods for authenticating API requests.', 7),
    ('User Experience', 'Improving user experience with thoughtful design.', 12);