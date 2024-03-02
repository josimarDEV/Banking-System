-- criar tabelas para o banco de dados

CREATE TABLE IF NOT EXISTS tipo_conta ( -- cria uma tabela si  ela nao existe, com os campos abaixo
    id_tipo_conta SERIAL, -- serial  é um número inteiro auto-incrementado
    tipo_conta_tipo VARCHAR(20) --  varchar é um campo que pode ter até 20 caracteres e só aceita letras. numeros podem ser colocados só que transorme em uma string antes
);

CREATE TABLE IF NOT EXISTS status_conta (
    id_status_conta SERIAL,
    status_conta_status VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY, --  chave primaria e incrementada automaticamente
    nome VARCHAR(255) NOT NULL, -- campo obrigatório com no mínimo 1 caracter e até 255 possíveis.
    cpf VARCHAR(14) NOT NULL,
    email VARCHAR(255) NOT NULL,
    telefone CHAR(14) NOT NULL, --  pode ter apenas números e deve ser igual a 14 digitos
    data_nascimento CHAR(10),
    secret VARCHAR(1500),
    tipo_conta VARCHAR(15),
    status_conta VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS conta_poupanca (
    id SERIAL PRIMARY KEY,
    id_cliente INT, --  chave estrangeira que vai procurar pelo id da tabela clientes
    numero_banco CHAR(3),
    agencia_poupanca CHAR(4),
    conta_poupanca SERIAL,
    saldo DECIMAL(10,2) NOT NULL, --  decimal permite valores decimais com até 10 casas e 2 dígitos após o ponto
    tipo_conta VARCHAR(15),
    status_conta VARCHAR(15),
    historico JSONB, --  coluna do tipo jsonb
    FOREIGN KEY (id_cliente) REFERENCES clientes(id) --   chave estrangeira que vai procurar pelo id da tabela clientes, que armazena informações criadas lá
);

CREATE TABLE IF NOT EXISTS secret_alfa (
    id SERIAL PRIMARY KEY,
    id_cliente INT,
    alfa VARCHAR(1000),
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

