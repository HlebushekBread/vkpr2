-- Тестовая таблица, имитирующая учётную систему по добыче.
-- Реального источника нет, продукт ленится.
CREATE TABLE IF NOT EXISTS production_daily (
    record_date DATE NOT NULL,
    field_name  TEXT NOT NULL,
    well_id     TEXT NOT NULL,
    volume_bbl  NUMERIC NOT NULL
);

INSERT INTO production_daily (record_date, field_name, well_id, volume_bbl) VALUES
    ('2026-07-13', 'Северное',  'W-101', 842.5),
    ('2026-07-13', 'Северное',  'W-102', 611.2),
    ('2026-07-13', 'Южное',     'W-201', 1023.8),
    ('2026-07-13', 'Южное',     'W-202', 954.0),
    ('2026-07-14', 'Северное',  'W-101', 830.1),
    ('2026-07-14', 'Северное',  'W-102', 598.7),
    ('2026-07-14', 'Южное',     'W-201', 1010.4),
    ('2026-07-14', 'Южное',     'W-202', 940.6);
