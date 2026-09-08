from airflow.decorators import dag, task
from datetime import datetime


@dag(schedule = "@daily", start_date=datetime(2026, 1,1))
def dds_dag(): 

    @task
    def raw_data():
        from etl.pipelines.raw_pipeline import run_raw_pipeline
        run_raw_pipeline()


    @task 
    def gold_counter_matrix():
        from etl.pipelines.gold_counter_matrix_pipeline import run_gold_counter_matrix_pipeline
        run_gold_counter_matrix_pipeline() 


    @task 
    def gold_hero_stats(): 
        from etl.pipelines.gold_hero_stats_pipeline import run_gold_hero_stats_pipeline
        run_gold_hero_stats_pipeline() 


    @task
    def gold_synergy_matrix(): 
        from etl.pipelines.gold_synegy_matrix_pipeline import run_gold_synergy_matrix_pipeline
        run_gold_synergy_matrix_pipeline()


    raw_data() >> [gold_counter_matrix(), gold_hero_stats(), gold_synergy_matrix()]

dds_dag() 