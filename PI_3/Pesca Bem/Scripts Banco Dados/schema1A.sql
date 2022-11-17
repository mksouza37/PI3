DROP TABLE IF EXISTS anuncio;

CREATE TABLE anuncio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	foto BLOB NOT NULL,
    titulo TEXT NOT NULL,
    texto TEXT NOT NULL,
	cidade TEXT NOT NULL,
	estado TEXT NOT NULL,
	nomeAnunciante TEXT NOT NULL,
    dt_inclusao TEXT NOT NULL,
	telcont TEXT NOT NULL,
	usuarioCad TEXT NOT NULL,
	statusvigencia TEXT NOT NULL
);
