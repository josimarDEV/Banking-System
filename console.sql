CREATE TABLE IF NOT EXISTS tipo_conta (
    id_tipo_conta SERIAL PRIMARY KEY,
    tipo_conta_tipo VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS status_conta (
    id_status_conta SERIAL PRIMARY KEY,
    status_conta_status VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cpf VARCHAR(14) NOT NULL,
    email VARCHAR(255) NOT NULL,
    telefone CHAR(14) NOT NULL,
    data_nascimento CHAR(10),
    secret VARCHAR(3000),
    saldo DECIMAL(10,2) NOT NULL,
    id_tipo_conta INT,
    id_status_conta INT,
    FOREIGN KEY (id_tipo_conta) REFERENCES tipo_conta(id_tipo_conta),
    FOREIGN KEY (id_status_conta) REFERENCES status_conta(id_status_conta)
);

CREATE TABLE IF NOT EXISTS secret_alfa (
    id SERIAL PRIMARY KEY,
    id_cliente INT,
    alfa VARCHAR(2000),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id)
);

CREATE TABLE IF NOT EXISTS max_secret (
    id SERIAL PRIMARY KEY,
    id_cliente INT,
    max_alfa VARCHAR(255),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id)
);

CREATE TABLE IF NOT EXISTS min_secret (
    id SERIAL PRIMARY KEY,
    id_cliente INT,
    min_alfa VARCHAR(255),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id)
);

-- DROP TABLE secret_alfa;
-- DROP TABLE max_secret;
-- DROP TABLE min_secret;
-- DROP TABLE clientes;