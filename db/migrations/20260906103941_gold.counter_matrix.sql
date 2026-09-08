-- migrate:up
CREATE TABLE IF NOT EXISTS gold.counter_matrix(
    hero_1 UInt32,
    hero_2 UInt32,
    total_games UInt64, 
    wins_against UInt64, 
    win_rate_hero1 Float32, 
    win_rate_hero2 Float32, 
    calculated_at DateTime DEFAULT now() 
)

ENGINE = ReplacingMergeTree(calculated_at)
ORDER BY (hero_1, hero_2)
PARTITION BY toYYYYMM(calculated_at);

-- migrate:down
DROP TABLE IF EXISTS gold.counter_matrix;

