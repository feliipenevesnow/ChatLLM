CREATE DATABASE uni1500_negocio;

USE uni1500_negocio;

CREATE TABLE Vendedores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    telefone VARCHAR(50)
);

CREATE TABLE Fazendas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    estado VARCHAR(50),
    municipio VARCHAR(255)
);

CREATE TABLE Bois (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    peso FLOAT,
    altura FLOAT,
    comprimento FLOAT,
    idade INT,
    pelagem VARCHAR(100),
    origem VARCHAR(100),
    fazenda_id INT,
    FOREIGN KEY (fazenda_id) REFERENCES Fazendas(id)
);

CREATE TABLE Inseminadores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

CREATE TABLE Protocolos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    duracao INT,
    implante VARCHAR(255),
    fornecedor VARCHAR(255),
    gnrh BOOLEAN,
    pgf_dose FLOAT,
    pgf_marca VARCHAR(255),
    ce_dose FLOAT,
    ecg_dose FLOAT,
    ecg_marca VARCHAR(255)
);

CREATE TABLE Vendas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendedor_id INT,
    fazenda_id INT,
    protocolo_id INT,
    data_venda DATE,
    quantidade INT,
    valor_total DECIMAL(10, 2),
    FOREIGN KEY (vendedor_id) REFERENCES Vendedores(id),
    FOREIGN KEY (fazenda_id) REFERENCES Fazendas(id),
    FOREIGN KEY (protocolo_id) REFERENCES Protocolos(id)
);

CREATE TABLE Inseminacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    boi_id INT,
    protocolo_id INT,
    inseminador_id INT,
    data DATE,
    resultado BOOLEAN,
    vendedor_id INT,
    FOREIGN KEY (boi_id) REFERENCES Bois(id),
    FOREIGN KEY (protocolo_id) REFERENCES Protocolos(id),
    FOREIGN KEY (inseminador_id) REFERENCES Inseminadores(id),
    FOREIGN KEY (vendedor_id) REFERENCES Vendedores(id)
);

CREATE TABLE Visitas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fazenda_id INT,
    vendedor_id INT,
    data_visita DATE,
    observacoes TEXT,
    FOREIGN KEY (fazenda_id) REFERENCES Fazendas(id),
    FOREIGN KEY (vendedor_id) REFERENCES Vendedores(id)
);

USE uni1500_negocio;

-- Inserir dados na tabela Vendedores
INSERT INTO Vendedores (nome, telefone) VALUES
('Carlos Silva', '1234-5678'),
('Ana Pereira', '8765-4321'),
('Marcos Souza', '9876-5432');

-- Inserir dados na tabela Fazendas
INSERT INTO Fazendas (nome, estado, municipio) VALUES
('Fazenda Boa Vista', 'MG', 'Belo Horizonte'),
('Fazenda Primavera', 'SP', 'Ribeirão Preto'),
('Fazenda Esperança', 'GO', 'Goiânia');

-- Inserir dados na tabela Bois
INSERT INTO Bois (nome, peso, altura, comprimento, idade, pelagem, origem, fazenda_id) VALUES
('Boi Bravo', 450.5, 1.50, 2.0, 3, 'Preta', 'Local', 1),
('Boi Manso', 480.3, 1.55, 2.1, 4, 'Marrom', 'Importada', 2),
('Boi Forte', 500.8, 1.60, 2.2, 5, 'Branca', 'Local', 3);

-- Inserir dados na tabela Inseminadores
INSERT INTO Inseminadores (nome) VALUES
('José dos Santos'),
('Paulo de Almeida'),
('Rita de Cássia');

-- Inserir dados na tabela Protocolos
INSERT INTO Protocolos (nome, duracao, implante, fornecedor, gnrh, pgf_dose, pgf_marca, ce_dose, ecg_dose, ecg_marca) VALUES
('Protocolo A', 10, 'Implante X', 'Fornecedor A', TRUE, 1.5, 'Marca A', 2.0, 3.0, 'Marca B'),
('Protocolo B', 12, 'Implante Y', 'Fornecedor B', FALSE, 2.0, 'Marca C', 2.5, 3.5, 'Marca D');

-- Inserir dados na tabela Vendas
INSERT INTO Vendas (vendedor_id, fazenda_id, protocolo_id, data_venda, quantidade, valor_total) VALUES
(1, 1, 1, '2024-01-15', 100, 15000.00),
(2, 2, 2, '2024-02-20', 150, 22500.00),
(3, 3, 1, '2024-03-10', 120, 18000.00);

-- Inserir dados na tabela Inseminacoes
INSERT INTO Inseminacoes (boi_id, protocolo_id, inseminador_id, data, resultado, vendedor_id) VALUES
(1, 1, 1, '2024-01-20', TRUE, 1),
(2, 2, 2, '2024-02-25', FALSE, 2),
(3, 1, 3, '2024-03-15', TRUE, 3);

-- Inserir dados na tabela Visitas
INSERT INTO Visitas (fazenda_id, vendedor_id, data_visita, observacoes) VALUES
(1, 1, '2024-01-10', 'Tudo em ordem.'),
(2, 2, '2024-02-18', 'Recomendada melhoria no manejo.'),
(3, 3, '2024-03-08', 'Verificadas condições adequadas.');
