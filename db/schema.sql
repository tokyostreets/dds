
--
-- Database schema
--

CREATE DATABASE IF NOT EXISTS default;

CREATE MATERIALIZED VIEW default.mv_hero_picks_cleaned TO silver.hero_picks_cleaned
(
    `match_id` UInt64,
    `hero_id` UInt32,
    `team` LowCardinality(String),
    `won` Bool,
    `match_mode` LowCardinality(String),
    `average_badge` UInt32,
    `start_time` DateTime,
    `processed_at` DateTime
)
AS SELECT
    match_id,
    hero_id,
    team,
    won,
    match_mode,
    average_badge,
    start_time,
    now() AS processed_at
FROM raw.hero_picks;

CREATE TABLE default.schema_migrations
(
    `version` String,
    `ts` DateTime DEFAULT now(),
    `applied` UInt8 DEFAULT 1
)
ENGINE = ReplacingMergeTree(ts)
PRIMARY KEY version
ORDER BY version
SETTINGS index_granularity = 8192;


--
-- Dbmate schema migrations
--

INSERT INTO default.schema_migrations (version) VALUES
    ('20260830075408'),
    ('20260830090311'),
    ('20260902110140'),
    ('20260902110933'),
    ('20260902114810'),
    ('20260906103941'),
    ('20260907073122');
