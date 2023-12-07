from playwright.sync_api import Playwright, sync_playwright, Locator, Page
import csv

url = "https://pogoda21.ru/arch.php"


def parse_table(table: Locator, year: int, month: int) -> None:
    rows = table.locator("tr")
    rows_count = rows.count()
    if month == 2 and year % 4 != 0:
        rows_count = rows_count - 1

    filename = f'Архив_погоды_{month}_{year}.csv'

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Дата', 'Минимум', 'Средняя', 'Максимум', 'Отклонение_от_нормы', 'Осадки'])
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


def iterate_archive(page: Page, yearStart: int, yearEnd: int) -> None:
    for year in range(yearStart, yearEnd + 1):
        for month in range(1, 13):
            page.goto(f'{url}?month={month}&year={year}')
            table = page.locator('#arch_table table')
            parse_table(table, year, month)


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(url)

    iterate_archive(page, yearStart=int(input('Введите год начала: ')), yearEnd=int(input('Введите год конца: ')))

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
