from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def parse_matches(matches: list | None) -> list[dict] | None:
    if matches is not None: 
        clean_data = []

        for item in matches: 
            if (match_id := item.get("match_id")) is None: continue
            if (match_mode := item.get("match_mode")) is None: continue
            if (players_dict := item.get("players", [])) is None: continue
            if (start_time := item.get("start_time")) is None: continue
            average_badge = item.get("average_badge") or 0 # API sends null as None that's why there is no check

            try: 
                for player in players_dict: 
                    if (hero_id := player.get("hero_id")) is None: continue
                    if (team := player.get("team")) is None: continue
                    won = (player["team"] == item["winning_team"])
                    

                    clean_match_data = { 
                        "match_id" : int(match_id), 
                        "match_mode": match_mode,
                        "average_badge" : average_badge, 
                        "hero_id" : hero_id,
                        "team" : team,
                        "won" : won,
                        "start_time" : datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                    }

                    clean_data.append(clean_match_data)
            except KeyError as e: 
                logger.error(f"Key Error: {e}")
                continue

        return clean_data

    else:
        logger.error("No Valid Data")
        return None 
        

