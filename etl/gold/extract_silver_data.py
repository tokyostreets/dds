import logging
import clickhouse_connect.driver.exceptions as e 
from clickhouse_connect.driver.query import QueryResult

from clients.db.clickhouse_client import ClickHouseConnection

logger = logging.getLogger(__name__)

def extract_silver_data_synergy() -> QueryResult: 
    client = ClickHouseConnection.get_client()

    data = client.query("""
            SELECT 
                shpc.hero_id AS hero_1,
                shpc2.hero_id AS hero_2, 
                COUNT(*) AS total_games, 
                SUM(shpc.won) AS wins, 
                ROUND(SUM(shpc.won) / COUNT(*), 3) AS win_rate
            FROM silver.hero_picks_cleaned AS shpc
            INNER JOIN silver.hero_picks_cleaned AS shpc2 
                ON shpc.match_id = shpc2.match_id
            AND shpc.team = shpc2.team
            WHERE shpc.hero_id < shpc2.hero_id
            GROUP BY hero_1, hero_2
        """)

    return data

def extract_silver_data_counter() -> QueryResult: 
    client = ClickHouseConnection.get_client() 

    data = client.query(
        """
        SELECT
            CASE WHEN win_rate_hero1 > 0.5 THEN h1 ELSE h2 END AS hero_1,
            CASE WHEN win_rate_hero1 > 0.5 THEN h2 ELSE h1 END AS hero_2,
            total_games,
            wins_against,
            win_rate_hero1,
            win_rate_hero2

        FROM (
                SELECT 
            shpc.hero_id AS h1, 
            shpc2.hero_id AS h2,
            COUNT(*) AS total_games, 
            SUM(shpc.won) AS wins_against, 
            ROUND(SUM(shpc.won) / COUNT(*), 3) AS win_rate_hero1,
            ROUND(1 - SUM(shpc.won) / COUNT(*), 3) AS win_rate_hero2
            FROM silver.hero_picks_cleaned AS shpc
            INNER JOIN silver.hero_picks_cleaned AS shpc2
                ON shpc.match_id = shpc2.match_id 
            WHERE shpc.hero_id < shpc2.hero_id
            AND shpc.team <> shpc2.team
            GROUP BY h1, h2
            )
        """
    )

    return data

def extract_silver_data_hero_stats() -> QueryResult: 
    client = ClickHouseConnection.get_client() 

    data = client.query(
        """
        SELECT -- EXTRACT SILVER DATA HEROES
            shpc.hero_id AS hero_id,
            ROUND(SUM(shpc.won) / COUNT(*), 3) AS win_rate,
            ROUND(COUNT(*) / SUM(COUNT(*)) OVER(), 4)AS pick_rate,
            SUM(shpc.won) AS winning_games,
            COUNT(*) AS total_games
        FROM silver.hero_picks_cleaned as shpc
        GROUP BY hero_id
        """
    )

    return data 