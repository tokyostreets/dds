-- migrate:up
CREATE TABLE IF NOT EXISTS gold.hero_stats( 
    hero_id UInt32,
    win_rate Float32, 
    pick_rate Float32,
    winning_games UInt64, 
    total_games UInt64, 
    calculated_at DateTime DEFAULT now()
)
ENGINE = ReplacingMergeTree(calculated_at)
ORDER BY (hero_id)
PARTITION BY toYYYYMM(calculated_at);
-- migrate:down
DROP TABLE IF EXISTS gold.hero_stats;


