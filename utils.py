import json
import pandas as pd


def convert_result_to_csv():
    print("Converting result to CSV")
    with open("patterns.json", "r") as file:
        patterns = json.load(file)

    df = pd.DataFrame(patterns)
    df.to_csv("patterns.csv", index=False)
