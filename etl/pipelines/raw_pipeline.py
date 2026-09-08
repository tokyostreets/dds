from etl.clients.db.clickhouse_client import ClickHouseConnection 
from etl.clients.api.deadlock_api_client import fetch_bulk_metadata
from etl.raw.extract_api_data import parse_matches
from etl.raw.load import load_raw_data

def run_raw_pipeline(): 
    #TODO: REDIS CACHE FOR CHECKING last_match_id
    client = ClickHouseConnection.get_client() 
    last_match_id = client.query("SELECT MAX(match_id) FROM raw.hero_picks").result_rows[0][0] or 0 

    matches = fetch_bulk_metadata(min_match_id=last_match_id)
    clean_data = parse_matches(matches=matches)
    load_raw_data(clean_data)

    
if __name__ == "__main__": 
    run_raw_pipeline() 
