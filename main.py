import csv
import sys
from scraper import parse_page, print_page, to_csv

if __name__ == '__main__':

    parse_pages = int(sys.argv[1])
    store_report = sys.argv[2] if len(sys.argv) == 3 else 'report.csv'

    # limit to 1 and 200 pages
    # default 30
    parse_pages = parse_pages if parse_pages >= 1 and parse_pages <= 200 else 30

    print("Parsing {parse_pages} pages...".format(parse_pages=parse_pages))

    scrape_url = 'https://www.skinnytaste.com/'

    parsed = []

    while scrape_url is not None and len(parsed) < parse_pages:
        _page = parse_page(scrape_url)
        scrape_url = _page.navigation.next_link
        parsed.append(_page)

    print("Saving report {store_report}...".format(store_report=store_report))

    with open(store_report, 'w', newline='', encoding='utf-8') as csvreport:
        csv_writer = csv.writer(csvreport, delimiter=',', quoting=csv.QUOTE_MINIMAL)

        current_page = 0
        for page in parsed:
            csv_pages = to_csv(page)
            # print headers only on first page
            for csv_row in csv_pages if current_page == 0 else csv_pages[1:]:
                csv_writer.writerow(csv_row)
            current_page += 1


