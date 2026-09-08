import enum
import logging
import clickhouse_connect.driver.exceptions as e 
from etl.clients.db.clickhouse_client import ClickHouseConnection
from clickhouse_connect.driver.exceptions import ClickHouseError, OperationalError, DataError, ProgrammingError
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter


logger = logging.getLogger(__name__)


class GoldTable(enum.Enum):
    SYNERGY = ("synergy_matrix", ["hero_1", "hero_2", "total_games", "wins", "win_rate"])
    COUNTER = ("counter_matrix", ["hero_1", "hero_2", "total_games", "wins_against", "win_rate_hero1", "win_rate_hero2"])
    HERO_STATS = ("hero_stats", ["hero_id", "win_rate", "pick_rate", "winning_games", "total_games"])

    def __init__(self, table_name: str, columns: list[str]):
        self.table_name = table_name
        self.columns = columns

@retry(
    retry=retry_if_exception_type((OperationalError)),
    stop=stop_after_attempt(5),
    wait=wait_exponential_jitter(initial=1, max=10, jitter=2),
    reraise=True
)
def load_gold_data(data: list[dict] | None, table: GoldTable) -> None: 
    if data is not None:
        try: 
            client = ClickHouseConnection.get_client()
            column_names = table.columns
            rows = [list(row) for row in data]
            client.insert(table=f"gold.{table.table_name}", data=rows, column_names=column_names)
            logger.info("Insert Batch Gold Data Complete")


        except (DataError, ProgrammingError) as er:
            logger.error(f"Insert Failed: {er} : retrying")
            raise

        except (OperationalError, ClickHouseError) as er: 
            logger.error(f"Insert Failed: {er} : Need Retry")  
            raise 


    else: 
        logger.error("No valid data")

