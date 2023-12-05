from playwright.sync_api import Playwright, sync_playwright, Locator, Page

url = "https://pogoda21.ru/arch.php"

def parse_table(table: Locator) -> None:
    rows = table.locator("tr")
    rows_count = rows.count()
    for i in range(2, rows_count):
        row = rows.nth(i)
        cells = row.locator("td")
        cellData = []
        for j in range(cells.count()):
            cell = cells.nth(j)
            if not cell.text_content():
                continue
            cellData.append(float(cell.text_content()))
        print(cellData)

def iterate_archive(page: Page, yearStart: int, yearEnd: int) -> None:
    for year in range(yearStart, yearEnd + 1):
        for month in range(1, 12+1):
            page.goto(f'{url}?month={month}&year={year}')
            table = page.locator("#arch_table > tbody > tr:nth-child(3) > td > table")
            parse_table(table)

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(url)

    iterate_archive(page, 2022, 2022)

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)