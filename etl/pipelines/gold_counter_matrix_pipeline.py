from etl.gold.extract_silver_data import extract_silver_data_counter
from etl.gold.transform import parse_silver_data
from etl.gold.load import load_gold_data, GoldTable

def run_gold_counter_matrix_pipeline(): 
    data = extract_silver_data_counter() 
    parsed_data = parse_silver_data(data=data)
    load_gold_data(parsed_data, GoldTable.COUNTER)
    

if __name__ == "__main__": 
    run_gold_counter_matrix_pipeline()