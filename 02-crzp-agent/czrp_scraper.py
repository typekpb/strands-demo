import subprocess
from strands import tool
from playwright.async_api import async_playwright


async def install_browsers_if_missing():
    """Install browsers if not already installed."""
    try:
        from playwright._impl._driver import get_driver_executable
        get_driver_executable("chromium")
    except Exception:
        print("Installing Playwright browsers...")
        subprocess.run(["playwright", "install", "chromium"], check=True)


@tool
async def thesis_fetch(search_term: str) -> str:
    """
    Fetches diploma or bachelors thesis from the site: https://opac.crzp.sk
    based on the specified search word.

    Args:
        search_term (str): The search term in https://opac.crzp.sk

    Returns:
        str: The result is in csv format, having: Title, whether pdf is available and keywords. The 1.st row is a header.
    """

    print("Fetching diploma or bachelors thesis for word")

    await install_browsers_if_missing()

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--no-sandbox"]
        )
        page = await browser.new_page()

        await page.goto(
            'https://opac.crzp.sk/?seo=CRZP-H%C4%BEadanie&fn=AdvancedSearchChildQ17GQP'
        )

        # Wait for search input, type query, load results
        await page.wait_for_selector('input[placeholder="Zadajte text pre hľadanie..."]', timeout=10000)
        await page.fill('input[placeholder="Zadajte text pre hľadanie..."]', search_term)
        await page.keyboard.press('Enter')
        await page.wait_for_load_state('networkidle')

        records = page.locator('div.well-sm.horizontal-rule')
        count = await records.count()

        print(f"Found {count} records")

        results = ["Title|PDF Available|Keywords"]

        for i in range(count):
            record = records.nth(i)
            title = await record.locator("a.no-decoration.h4.inline").inner_text()
            pdf_exists = await record.locator('img[title="Dostupné PDF"]').count() > 0
            keywords = await record.locator("a.display-subject").all_inner_texts()

            results.append(f"{title}|{pdf_exists}|{keywords}")

        await browser.close()

        return "\n".join(results)
