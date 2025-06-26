import argparse

from analysis.analyzer import run_analysis, run_analysis_by_levels

def main():
    parser = argparse.ArgumentParser(description="Python technologies statistics from work.ua")
    parser.add_argument(
        "--mode",
        choices=["sync", "async"],
        default="sync",
        help="Choose scraping mode: sync or async (default: sync)"
    )
    args = parser.parse_args()

    if args.mode == "sync":
        from scraping.work_ua_parser import fetch_vacancies
        print("[INFO] Running in SYNC mode")
        fetch_vacancies()
        input_path = 'data/raw/work_ua_vacancies.json'
    else:
        from scraping.async_work_ua_parser import run_async_scraper
        print("[INFO] Running in ASYNC mode")
        run_async_scraper()
        input_path = 'data/raw/work_ua_vacancies_async.json'

    run_analysis(input_path)
    run_analysis_by_levels(input_path)

if __name__ == "__main__":
    main()
