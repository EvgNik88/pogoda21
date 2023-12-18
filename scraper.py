from playwright.sync_api import Playwright, sync_playwright, Locator, Page
import csv
import argparse

url = "https://pogoda21.ru/arch.php"


def parse_table(table: Locator, year: int, month: int, writer: csv.writer) -> None:
    rows = table.locator("tr")
    rows_count = rows.count()
    if month == 2 and year % 4 != 0:
        rows_count = rows_count - 1

    for i in range(2, rows_count):
        row = rows.nth(i)
        cells = row.locator("td")
        cell_data = []
        for j in range(cells.count()):
            cell = cells.nth(j)
            if cell.text_content():
                cell_data.append(float(cell.text_content()))
        cell_data[0] = f'{str(i - 1).zfill(2)}.{str(month).zfill(2)}.{year}'
        writer.writerow(cell_data)
        print(*cell_data)


def iterate_archive(page: Page, year_of_start: int, year_of_end: int, writer: csv.writer) -> None:
    for year in range(year_of_start, year_of_end + 1):
        for month in range(1, 13):
            page.goto(f'{url}?month={month}&year={year}')
            table = page.locator('//*[@id="arch_table"]//table')
            parse_table(table, year, month, writer)


def run(playwright: Playwright, year_start: int, year_end: int, output_path: str) -> None:
    filename = f'{output_path}'

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Дата', 'Минимум', 'Средняя', 'Максимум', 'Отклонение_от_нормы', 'Осадки'])

        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)

        iterate_archive(page, year_of_start=year_start, year_of_end=year_end, writer=writer)

        context.close()
        browser.close()


parser = argparse.ArgumentParser(description="Аргументы командной строки")
parser.add_argument("--start", "-s", type=int, help="Год начала", default=2008)
parser.add_argument("--end", "-e", type=int, help="Год конца", default=2023)
parser.add_argument("--output", "-o", type=str, help="Путь сохранения файла", default='Архив погоды.csv')

args = parser.parse_args()

with sync_playwright() as playwright:
    run(playwright, year_start=args.start, year_end=args.end, output_path=args.output)
    print(f'Данные загружены в файл {str(args.output).split("/")[-1]}')
