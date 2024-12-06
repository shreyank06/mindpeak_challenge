import os
import pandas as pd
from dagster import op, job

# Step 1: Embedding Generation
@op
def run_embedding_generation():
    os.system("python3 embedding.py")
    return "Embeddings generated successfully."

# Step 2: Report Generation
@op
def run_report_generation(embedding_status: str):
    # embedding_status ensures this runs after `run_embedding_generation`
    os.system("python3.10 final_script.py")
    return "Reports generated successfully."

# Step 3: Aggregate Reports
@op
def aggregate_reports(report_status: str):
    # report_status ensures this runs after `run_report_generation`
    output_folder = "./output"
    txt_files = [f for f in os.listdir(output_folder) if f.endswith(".txt")]
    aggregated_data = []
    
    for txt_file in txt_files:
        file_path = os.path.join(output_folder, txt_file)
        with open(file_path, "r") as file:
            content = file.read()
        wsi_name = os.path.splitext(txt_file)[0]
        aggregated_data.append({"wsi_name": wsi_name, "report": content})
    
    # Save to CSV
    result_csv_path = os.path.join(output_folder, "result.csv")
    df = pd.DataFrame(aggregated_data)
    df.to_csv(result_csv_path, index=False)
    return f"Aggregated reports saved to {result_csv_path}"

# Define the Dagster Job
@job
def productionize_model_pipeline():
    embedding_status = run_embedding_generation()
    report_status = run_report_generation(embedding_status)
    aggregate_reports(report_status)
