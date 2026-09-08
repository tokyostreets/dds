import enum
import logging
import clickhouse_connect.driver.exceptions as e 
from clients.db.clickhouse_client import ClickHouseConnection

logger = logging.getLogger(__name__)

class GoldTable(enum.Enum):
    SYNERGY = ("synergy_matrix", ["hero_1", "hero_2", "total_games", "wins", "win_rate"])
    COUNTER = ("counter_matrix", ["hero_1", "hero_2", "total_games", "wins_against", "win_rate_hero1", "win_rate_hero2"])
    HERO_STATS = ("hero_stats", ["hero_id", "win_rate", "pick_rate", "winning_games", "total_games"])

    def __init__(self, table_name: str, columns: list[str]):
        self.table_name = table_name
        self.columns = columns


def load_gold_data(data: list[dict] | None, table: GoldTable) -> None: 
    if data is not None:
        try: 
            client = ClickHouseConnection.get_client()
            column_names = table.columns
            rows = [list(row) for row in data]
            client.insert(table=f"gold.{table.table_name}", data=rows, column_names=column_names)
            logger.info("Insert Batch Gold Data Complete")
        except e.OperationalError as er:
            #TODO: Retry Logic
            logger.error(f"Insert Gold Data Failed: {er}: Need Retry")
            raise

        except e.DataError as er: 
            logger.error(f"Gold Data Error: {er}")

        except e.ProgrammingError as er: 
            logger.error(f"Configuration Error: {er}") 

    else: 
        logger.error("No valid data")

