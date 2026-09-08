import logging
from clickhouse_connect.driver.exceptions import ClickHouseError, OperationalError, DataError, ProgrammingError
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter

from etl.clients.db.clickhouse_client import ClickHouseConnection

logger = logging.getLogger(__name__)

@retry( 
    retry=retry_if_exception_type((OperationalError)),
    stop=stop_after_attempt(5),
    wait=wait_exponential_jitter(initial=1, max=10, jitter=2),
    reraise=True
)
def load_raw_data(data: list[dict] | None) -> None: 
    if data is not None: 
        try: 
            client = ClickHouseConnection.get_client()
            column_names = ["match_id", "hero_id", "team", "won", "match_mode", "average_badge", "start_time"]
            
            rows = [[row[col] for col in column_names] for row in data]
            client.insert(table="raw.hero_picks", data=rows, column_names=column_names)
            logger.info("Insert Batch Complete")
        

        except (DataError, ProgrammingError) as er:
            logger.error(f"Insert Failed: {er} : retrying")
            raise

        except (OperationalError, ClickHouseError) as er: 
            logger.error(f"Insert Failed: {er} : Need Retry")  
            raise 

    else: 
        logger.error("No valid data")