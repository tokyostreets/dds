import logging
from clickhouse_connect.driver.query import QueryResult

logger = logging.getLogger(__name__)

def parse_silver_data(data: QueryResult) -> list[dict] | None:
    if data is not None: 
        list_data = data.result_rows
        logger.info("Silver data acquired the type `list`")
        return list_data

    else: 
        logger.error("No valid data")
        return None
