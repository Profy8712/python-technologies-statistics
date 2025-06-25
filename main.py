from scraping.work_ua_parser import fetch_vacancies
from analysis.analyzer import run_analysis, run_analysis_by_levels

if __name__ == "__main__":
    fetch_vacancies()
    run_analysis()
    run_analysis_by_levels()
