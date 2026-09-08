import logging
import clickhouse_connect.driver.exceptions as e 
from clients.db.clickhouse_client import ClickHouseConnection

logger = logging.getLogger(__name__)

def load_raw_data(data: list[dict] | None) -> None: 
    if data is not None: 
        try: 
            client = ClickHouseConnection.get_client()
            column_names = ["match_id", "hero_id", "team", "won", "match_mode", "average_badge", "start_time"]
            
            rows = [[row[col] for col in column_names] for row in data]
            client.insert(table="raw.hero_picks", data=rows, column_names=column_names)
            logger.info("Insert Batch Complete")
        
        except e.OperationalError as er: 
            #TODO: Retry Logic
            logger.error(f"Insert Failed: {er} : Need Retry")  
            raise 
        
        except e.DataError as er:
            logger.error(f"Data Error: {er}")

        except e.ProgrammingError as er: 
            logger.error(f"Configuration Error: {er}")
    else: 
        logger.error("No valid data")