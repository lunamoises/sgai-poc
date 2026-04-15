CREATE TABLE IF NOT EXISTS activos (
    id SERIAL PRIMARY KEY, nombre VARCHAR(200) NOT NULL,
    codigo VARCHAR(50) UNIQUE NOT NULL, categoria VARCHAR(100),
    estado VARCHAR(50) DEFAULT 'activo', created_at TIMESTAMPTZ DEFAULT NOW()
);
INSERT INTO activos (nombre,codigo,categoria) VALUES
  ('Laptop Dell XPS 15','LAP-001','Computación'),
  ('Proyector Epson EB','PRY-001','Audiovisual'),
  ('Switch Cisco 24p','NET-001','Networking')
ON CONFLICT DO NOTHING;
