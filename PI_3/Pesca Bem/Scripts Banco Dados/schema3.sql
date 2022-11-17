DROP TABLE IF EXISTS PostBlog;

CREATE TABLE Postblog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    date_posted DATETIME default current_timestamp NOT NULL,
    content TEXT NOT NULL,
    user_id INTEGER NOT NULL
);
