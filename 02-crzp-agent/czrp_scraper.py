import subprocess
from strands import tool
from playwright.async_api import async_playwright
import os
import tempfile

async def install_browsers_if_missing():
    """Install browsers if not already installed."""
    try:
        from playwright._impl._driver import get_driver_executable
        get_driver_executable("chromium")
    except Exception:
        # print("Installing Playwright browsers...")
        subprocess.run(["playwright", "install", "chromium"], check=True)

@tool
async def thesis_fetch(search_term: str) -> str:
    """
    Fetches diploma or bachelors thesis from the site: https://opac.crzp.sk
    based on the specified search term.

    Args:
        search_term (str): The search term in https://opac.crzp.sk

    Returns:
        str: The result is in csv format, having: Title, description and detail URL. The 1.st row is a header.
    """
    await install_browsers_if_missing()

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            # headless=False,
            args=["--no-sandbox"]
        )
        page = await browser.new_page()

        await page.goto('https://opac.crzp.sk/?seo=CRZP-H%C4%BEadanie&fn=AdvancedSearchChildQ17GQP')

        # Wait for search input, type query, load results
        await page.wait_for_selector('input[placeholder="Zadajte text pre hľadanie..."]', timeout=10000)
        await page.fill('input[placeholder="Zadajte text pre hľadanie..."]', search_term)
        await page.keyboard.press('Enter')
        await page.wait_for_load_state('networkidle')

        results = ["Title|Description|Detail URL"]

        async with page.context.expect_page() as new_page_info:
            await page.get_by_text('RSS').click()

        new_tab = await new_page_info.value
        await new_tab.wait_for_load_state()

        # Parse the feed
        records = new_tab.locator('item')
        rss_count = await records.count()

        print(f"Found {rss_count} RSS records")

        for i in range(rss_count):
            record = records.nth(i)
            link = await record.locator("link").text_content()
            description = await record.locator("description").text_content()
            title = await record.locator("title").text_content()
            results.append(f"{title}|{description}|{link}|")

        await browser.close()
        return "\n".join(results)

@tool
async def thesis_abstract_fetch(detail_link: str) -> str:
    """
    Fetches the abstract of the specific diploma or bachelors thesis from the site: https://opac.crzp.sk
    based on the thesis reference.
    Abstract is kept for all the thesis (even if it has no pdf attached in the portal).

    Args:
        detail_link (str): the URL of the previously fetched thesis from the site: https://opac.crzp.sk.

    Returns:
        str: The result is in csv format, having: Abstract in all the provided languages (primary is on top). The 1.st row is a header.
    """
    await install_browsers_if_missing()

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            # headless=False,
            args=["--no-sandbox"]
        )
        page = await browser.new_page()

        await page.goto(detail_link)

        # Wait for search input, type query, load results
        await page.wait_for_selector('div.well.well-sm', timeout=10000)

        records = page.locator('div.well.well-sm')
        count = await records.count()

        print(f"Found {count} records")

        results = ["Abstract"]

        for i in range(count):
            record = records.nth(i)
            abstract = await record.inner_text()
            results.append(f"{abstract}")

        await browser.close()

        return "\n".join(results)


@tool
async def thesis_retrieve_pdf_if_available(detail_link: str) -> str:
    """
    Retrieves the pdf of diploma or bachelors thesis from the site: https://opac.crzp.sk
    based on the thesis reference.
    pdf is optional, so might not bre present for specific thesis.
    if it's available, reference to local pdf will be returned.

    Args:
        detail_link (str): the URL of the previously fetched thesis from the site: https://opac.crzp.sk.
    Returns:
        str: local pdf file, if available. Otherwise, returns None.
    """
    await install_browsers_if_missing()

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            # headless=False,
            headless=True,
            args=["--no-sandbox"]
        )
        page = await browser.new_page()

        await page.goto(detail_link)

        # Wait for search input, type query, load results
        await page.wait_for_selector('div.well.well-sm', timeout=10000)

        pdf_button = page.locator("a", has_text="Stiahnuť prácu (pdf)")

        if await pdf_button.count() > 0:
            await pdf_button.click()

            # Accept cookies if present
            cookie_label = page.locator("#cookie-bar label")

            if await cookie_label.count() > 0 and await cookie_label.is_visible():
                await cookie_label.click()
                print("Cookies banner clicked.")
            else:
                print("Cookies banner not present — continuing.")

            open_btn = page.get_by_text("Otvoriť v novom okne/stiahnuť súbor", exact=True)

            async with page.expect_download() as download_info:
                await open_btn.click()
            download = await download_info.value

            # Use filename suggested by server
            filename = download.suggested_filename

            # Save into system temp folder
            tmp_dir = tempfile.gettempdir()
            file_path = os.path.join(tmp_dir, filename)

            # Save file
            await download.save_as(file_path)
            print("Downloaded to:", file_path)
            return file_path

        return None
