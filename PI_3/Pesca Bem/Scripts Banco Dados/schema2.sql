DROP TABLE IF EXISTS empresas;

CREATE TABLE empresas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cnpj TEXT NOT NULL,
    cidade TEXT NOT NULL,
    estado TEXT NOT NULL,
    ramo TEXT NOT NULL,
    conduta TEXT NOT NULL
);

