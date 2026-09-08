-- migrate:up
CREATE TABLE IF NOT EXISTS silver.hero_picks_cleaned(
    match_id    UInt64,
    hero_id     UInt32,
    team        LowCardinality(String),
    won         Bool, 
    match_mode  LowCardinality(String),
    average_badge   UInt32, 
    start_time  DateTime,
    processed_at DateTime DEFAULT now()
)

ENGINE = ReplacingMergeTree(processed_at)
ORDER BY (match_id, hero_id)
PARTITION BY toYYYYMM(start_time);

-- migrate:down
DROP TABLE IF EXISTS silver.hero_picks_cleaned;

