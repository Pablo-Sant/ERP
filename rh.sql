
--MODULO DE RH
CREATE TABLE rh.funcoes (
    id INTEGER PRIMARY KEY,
    nome CHAR(50) NOT NULL,
    descricao CHAR(200)
);

CREATE TABLE rh.colaboradores (
    id INTEGER PRIMARY KEY,
    nome CHAR(100) NOT NULL,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    email CHAR(100),
    funcao_id INTEGER, -- referencia tabela funcoes
    data_contratacao DATE NOT NULL,
    carga_horaria INTEGER NOT NULL,
    data_de_nascimento DATE,
    data_de_recrutamento DATE NOT NULL,
    salario REAL NOT NULL,
    FOREIGN KEY (funcao_id) REFERENCES rh.funcoes(id)
);

CREATE TABLE rh.folha_pagamento (
    id INTEGER PRIMARY KEY,
    colaborador_id INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    salario_base REAL NOT NULL,
    descontos REAL,
    salario_liquido REAL NOT NULL,
    FOREIGN KEY (colaborador_id) REFERENCES rh.colaboradores(id)
);

CREATE TABLE rh.beneficios (
    id INTEGER PRIMARY KEY,
    nome CHAR(50) NOT NULL,
    descricao CHAR(200),
    valor REAL
);


CREATE TABLE rh.colaborador_beneficios (
    id INTEGER PRIMARY KEY,
    colaborador_id INTEGER NOT NULL,
    beneficio_id INTEGER NOT NULL,
    FOREIGN KEY (colaborador_id) REFERENCES rh.colaboradores(id),
    FOREIGN KEY (beneficio_id) REFERENCES rh.beneficios(id)
);

CREATE TABLE rh.recrutamento (
    id INTEGER PRIMARY KEY,
    colaborador_id INTEGER NOT NULL,
    data_recrutamento DATE NOT NULL,
    status CHAR(50) NOT NULL,
    observacoes CHAR(200),
    FOREIGN KEY (colaborador_id) REFERENCES rh.colaboradores(id)
);

CREATE TABLE rh.avaliacao_desempenho (
    id INTEGER PRIMARY KEY,
    colaborador_id INTEGER NOT NULL,
    data_avaliacao DATE NOT NULL,
    nota INTEGER NOT NULL,
    comentarios CHAR(200),
    FOREIGN KEY (colaborador_id) REFERENCES rh.colaboradores(id)
);


