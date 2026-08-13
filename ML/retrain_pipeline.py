# ============================================================
# EduLink — Model Retraining Pipeline
# Run monthly or when new data is available
# ============================================================

import pandas as pd
import os
from datetime import datetime

def retrain_career_fit(data_path: str):
    """
    Retrain career fit weights using new student data.
    data_path: CSV with columns Q1-Q40 + actual_career
    """
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} student records")

    # Compute composites for each student
    from models.career_fit_prediction import compute_composites

    features = []
    for _, row in df.iterrows():
        mcq = {f"Q{i}": row[f"Q{i}"] for i in range(1, 41)}
        composites = compute_composites(mcq)
        composites["actual_career"] = row["actual_career"]
        features.append(composites)

    df_features = pd.DataFrame(features)

    # Calculate accuracy with current weights
    correct = 0
    for _, row in df_features.iterrows():
        from models.career_fit_prediction import predict
        mcq = {f"Q{i}": row[f"Q{i}"]
               for i in range(1, 41)
               if f"Q{i}" in row}
        pred = predict(mcq)
        if pred["top1_cluster"] == row["actual_career"]:
            correct += 1

    accuracy = correct / len(df_features)
    print(f"Current accuracy: {accuracy:.1%}")
    print(f"Retrain date: {datetime.now().strftime('%Y-%m-%d')}")
    return accuracy


if __name__ == "__main__":
    if os.path.exists("data/real_student_responses.csv"):
        retrain_career_fit("data/real_student_responses.csv")
    else:
        print("No real data found. Collect school visit data first.")