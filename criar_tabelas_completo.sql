-- ============================================================
-- TABELA 1: users
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    tipo ENUM('admin','funcionaria') NOT NULL,
    telefone VARCHAR(20) DEFAULT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY username (username),
    KEY idx_users_telefone (telefone)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- TABELA 2: records
-- ============================================================
CREATE TABLE IF NOT EXISTS records (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    data DATE NOT NULL,
    hora_entrada TIME DEFAULT NULL,
    hora_saida TIME DEFAULT NULL,
    observacoes TEXT,
    PRIMARY KEY (id),
    UNIQUE KEY unico_registro_dia (user_id, data),
    KEY idx_records_user_data (user_id, data),
    KEY idx_records_data (data),
    CONSTRAINT records_ibfk_1 FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- TABELA 3: solicitacoes_correcao
-- ============================================================
CREATE TABLE IF NOT EXISTS solicitacoes_correcao (
    id INT NOT NULL AUTO_INCREMENT,
    funcionaria_id INT NOT NULL,
    data_solicitacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_registro DATE NOT NULL COMMENT 'Data do registro que precisa ser corrigido',
    tipo ENUM('entrada','saida','ambos') NOT NULL COMMENT 'Tipo de correção solicitada',
    horario_entrada TIME DEFAULT NULL COMMENT 'Horário de entrada informado',
    horario_saida TIME DEFAULT NULL COMMENT 'Horário de saída informado',
    justificativa TEXT NOT NULL COMMENT 'Motivo da solicitação',
    status ENUM('pendente','aprovado','rejeitado') DEFAULT 'pendente',
    observacao_admin TEXT COMMENT 'Observação do admin ao aprovar/rejeitar',
    data_processamento DATETIME DEFAULT NULL COMMENT 'Quando foi aprovado/rejeitado',
    PRIMARY KEY (id),
    UNIQUE KEY unique_solicitacao (funcionaria_id, data_registro, status),
    KEY idx_status (status),
    KEY idx_funcionaria (funcionaria_id),
    KEY idx_solicitacoes_status (status),
    CONSTRAINT solicitacoes_correcao_ibfk_1 FOREIGN KEY (funcionaria_id) REFERENCES users (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- TABELA 4: configuracoes_pagamento
-- ============================================================
CREATE TABLE IF NOT EXISTS configuracoes_pagamento (
    id INT NOT NULL AUTO_INCREMENT,
    tipo_dia VARCHAR(20) NOT NULL COMMENT 'Dia da semana (segunda, terca, quarta, quinta, sexta, sabado, domingo)',
    valor_hora DECIMAL(10,2) NOT NULL COMMENT 'Valor pago por hora trabalhada neste dia',
    data_criacao TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Quando foi criado',
    data_atualizacao TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Última alteração',
    atualizado_por VARCHAR(100) DEFAULT NULL COMMENT 'Nome do admin que alterou',
    ativo TINYINT(1) DEFAULT 1 COMMENT 'Permite desativar dias específicos no futuro',
    PRIMARY KEY (id),
    UNIQUE KEY tipo_dia (tipo_dia),
    KEY idx_tipo_dia (tipo_dia),
    KEY idx_ativo (ativo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Valores de pagamento configuráveis por dia da semana';

-- ============================================================
-- TABELA 5: historico_alteracoes
-- ============================================================
CREATE TABLE IF NOT EXISTS historico_alteracoes (
    id INT NOT NULL AUTO_INCREMENT,
    record_id INT DEFAULT NULL,
    data_alteracao DATETIME DEFAULT CURRENT_TIMESTAMP,
    hora_entrada_antiga TIME DEFAULT NULL,
    hora_saida_antiga TIME DEFAULT NULL,
    hora_entrada_nova TIME DEFAULT NULL,
    hora_saida_nova TIME DEFAULT NULL,
    alterado_por INT DEFAULT NULL,
    motivo VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- TABELA 6: records_backup
-- ============================================================
CREATE TABLE IF NOT EXISTS records_backup (
    id INT NOT NULL DEFAULT 0,
    user_id INT NOT NULL,
    data DATE NOT NULL,
    hora_entrada TIME DEFAULT NULL,
    hora_saida TIME DEFAULT NULL,
    observacoes TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- DADOS INICIAIS: configuracoes_pagamento
-- ============================================================
INSERT IGNORE INTO configuracoes_pagamento (tipo_dia, valor_hora, atualizado_por) VALUES
('segunda', 6.90, 'Sistema - Inicialização'),
('terca', 6.90, 'Sistema - Inicialização'),
('quarta', 6.90, 'Sistema - Inicialização'),
('quinta', 6.90, 'Sistema - Inicialização'),
('sexta', 6.90, 'Sistema - Inicialização'),
('sabado', 6.90, 'Sistema - Inicialização'),
('domingo', 10.00, 'Sistema - Inicialização');

