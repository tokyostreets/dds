from gold.extract_silver_data import extract_silver_data_hero_stats
from gold.transform import parse_silver_data
from gold.load import load_gold_data, GoldTable

def run_gold_hero_stats_pipeline(): 
    data = extract_silver_data_hero_stats() 
    parsed_data = parse_silver_data(data=data)
    load_gold_data(parsed_data, GoldTable.HERO_STATS)
    

if __name__ == "__main__": 
    run_gold_hero_stats_pipeline()