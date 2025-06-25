import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from config.config import TECHNOLOGIES, EXPERIENCE_LEVELS


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


def save_plot(tech_counter: dict, output_path: str, title: str) -> None:
    technologies = list(tech_counter.keys())
    counts = list(tech_counter.values())

    plt.figure(figsize=(12, 6))
    plt.bar(technologies, counts)
    plt.xticks(rotation=45, ha='right')
    plt.title(title)
    plt.xlabel("Technology")
    plt.ylabel("Number of Mentions")
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()
    print(f"[INFO] Plot saved to {output_path}")


def run_analysis(input_path: str):
    vacancies = load_vacancies(input_path)
    tech_counter = count_technologies(vacancies, TECHNOLOGIES)
    save_plot(tech_counter, 'diagrams/tech_demand_workua.png', "Total Technology Demand (All Levels)")

    df = pd.DataFrame(list(tech_counter.items()), columns=['Technology', 'Count'])
    print("\n=== TOTAL TECHNOLOGY USAGE ===")
    print(df.sort_values(by='Count', ascending=False).to_string(index=False))


def filter_vacancies_by_level(vacancies: list, level: str) -> list:
    level_lower = level.lower()
    return [
        v for v in vacancies
        if level_lower in v.get("title", "").lower() or
           level_lower in v.get("description", "").lower()
    ]


def run_analysis_by_levels(input_path: str):
    vacancies = load_vacancies(input_path)

    for level in EXPERIENCE_LEVELS:
        level_vacancies = filter_vacancies_by_level(vacancies, level)
        tech_counter = count_technologies(level_vacancies, TECHNOLOGIES)

        plot_path = f'diagrams/{level.lower()}_tech_demand_workua.png'
        title = f"{level} Technology Demand"
        save_plot(tech_counter, plot_path, title)

        df = pd.DataFrame(list(tech_counter.items()), columns=['Technology', 'Count'])
        print(f"\n=== {level.upper()} TECHNOLOGY USAGE ===")
        print(df.sort_values(by='Count', ascending=False).to_string(index=False))
