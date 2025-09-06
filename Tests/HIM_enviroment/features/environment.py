
from dotenv import load_dotenv
import os
import asyncio
from playwright.async_api import Playwright, async_playwright, expect

load_dotenv(dotenv_path="Tests/.env")
login=[{"usrnm":os.environ["username"],"pass":os.environ["password"]}]
url={"DEV/HCS":"https://hcs.pallas-ai.com.au/","SAN/HCS":"https://san-hcs-dev.imedx.com.au/"}

async def setup_login():
    playwright_engine = await async_playwright().start()
    browser = await playwright_engine.chromium.launch(headless=False)
    incognito = await browser.new_context()
    page = await incognito.new_page()

    # Go to the login page
    await page.goto(url["DEV/HCS"])

    # Perform login
    await page.get_by_role("textbox", name="Username").fill(login[0]["usrnm"])
    await page.get_by_role("textbox", name="Password").fill(login[0]["pass"])
    await page.get_by_role("button", name="Log In").click()
    await asyncio.sleep(2)

    return playwright_engine,browser,incognito,page

def before_all(context):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    context.loop = loop
    context.playwright, context.browser, context.context, context.page = loop.run_until_complete(setup_login())

def after_all(context):
    # Clean up
    context.loop.run_until_complete(context.browser.close())
    context.loop.run_until_complete(context.playwright.stop())


