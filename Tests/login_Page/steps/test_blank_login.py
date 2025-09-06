url={"DEV/HCS":"https://hcs.pallas-ai.com.au/","SAN/HCS":"https://san-hcs-dev.imedx.com.au"}
from playwright.async_api import Playwright, async_playwright, expect
import asyncio
from behave import given, when, then

async def given_setup_page(headless=False):
    playwright_engine= await async_playwright().start()
    browser= await playwright_engine.chromium.launch(headless=False)  # lunch the browser chroumium
    incognito = await browser.new_context()
    page = await incognito.new_page()
    return playwright_engine,browser,incognito,page

@given("url for login provided")
def step_open_browser(context):
    loop = asyncio.new_event_loop() 
    asyncio.set_event_loop(loop) #Sets the given event loop loop as the current event loop for the current OS thread.
    context.playwright_engine, context.browser, context.incognito, context.page = loop.run_until_complete(given_setup_page(headless=False))    

@when("goto to the login button click login button")
def step_goto_login_button(context):
    page = context.page
    loop = asyncio.get_event_loop() #Event Loop	 The engine that runs async tasks (like a CPU scheduler) Returns the current event loop for the current OS thread.
    loop.run_until_complete(page.goto(url["DEV/HCS"]))
    loop.run_until_complete(page.get_by_role("button", name="Log In").click())
    loop.run_until_complete(asyncio.sleep(3))

@then("Alert msg shown for required user_id and password")
def step_check_blank_alert(context):
    page = context.page
    loop = asyncio.get_event_loop()
    loop.run_until_complete(expect(page).get_by_role("alert").to_be_visible())