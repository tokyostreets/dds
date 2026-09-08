import requests
import logging

from etl.config.config import settings
 
logger = logging.getLogger(__name__)

def fetch_bulk_metadata(min_match_id: int) -> list | None: 
    try:
        search_params = {"min_match_id": min_match_id, "include_player_info": "true"}
        response = requests.get(f'{settings.DEADLOCK_API_BASE_URL}/v1/matches/metadata', params=search_params)
        
        if response.status_code == 200: 
            data = response.json()
            return data

        else: 
            logger.error(f"Error: {response.status_code}")
            return None

    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error: {e}")
        return None
    except requests.exceptions.Timeout as e: 
        logger.error(f"Timeout error: {e}")
        return None
    except requests.exceptions.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return None