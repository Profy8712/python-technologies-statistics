import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from config.config import TECHNOLOGIES

def load_vacancies(filepath: str) -> list:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"{filepath} does not exist")
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def count_technologies(vacancies: list, tech_list: list) -> dict:
    counter = {tech: 0 for tech in tech_list}
    for vacancy in vacancies:
        description = vacancy.get("description", "").lower()
        for tech in tech_list:
            if tech.lower() in description:
                counter[tech] += 1
    return counter

def save_plot(tech_counter: dict, output_path: str) -> None:
    technologies = list(tech_counter.keys())
    counts = list(tech_counter.values())

    plt.figure(figsize=(12, 6))
    plt.bar(technologies, counts)
    plt.xticks(rotation=45, ha='right')
    plt.title("Technology Mentions in Python Job Listings (work.ua)")
    plt.xlabel("Technology")
    plt.ylabel("Number of Mentions")
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Plot saved to {output_path}")

def run_analysis():
    input_path = 'data/raw/work_ua_vacancies.json'
    output_plot_path = 'diagrams/tech_demand_workua.png'

    vacancies = load_vacancies(input_path)
    tech_counter = count_technologies(vacancies, TECHNOLOGIES)
    save_plot(tech_counter, output_plot_path)

    df = pd.DataFrame(list(tech_counter.items()), columns=['Technology', 'Count'])
    print(df.sort_values(by='Count', ascending=False).to_string(index=False))
