DROP TABLE IF EXISTS Post;

CREATE TABLE Post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    date_posted DATETIME default current_timestamp NOT NULL,
    content TEXT NOT NULL,
    user_id INTEGER NOT NULL
);
