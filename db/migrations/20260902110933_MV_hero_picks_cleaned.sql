-- migrate:up
CREATE MATERIALIZED VIEW mv_hero_picks_cleaned TO silver.hero_picks_cleaned AS 
SELECT match_id, hero_id, team, won, match_mode, average_badge, start_time, now() as processed_at FROM raw.hero_picks
-- migrate:down
DROP MATERIALIZED VIEW IF EXISTS mv_hero_picks_cleaned