CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    text TEXT
);

INSERT INTO notes (text) VALUES
    ('Nota 1 desde la BD'),
    ('Otra nota desde DB');
