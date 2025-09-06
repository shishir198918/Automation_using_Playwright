login=[{"usrnm":"Sai","pass":"Sairam@123"}]
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



@given("url for login page provided")
def step_open_browser(context):
    loop = asyncio.new_event_loop() 
    asyncio.set_event_loop(loop) #Sets the given event loop loop as the current event loop for the current OS thread.
    context.playwright_engine, context.browser, context.incognito, context.page = loop.run_until_complete(given_setup_page(headless=False))

@when("goto the url for login page entre valid username and password")
def step_login(context):
    page = context.page
    loop = asyncio.get_event_loop() #Event Loop	 The engine that runs async tasks (like a CPU scheduler) Returns the current event loop for the current OS thread.
    loop.run_until_complete(page.goto(url["DEV/HCS"]))
    
    loop.run_until_complete(page.get_by_role("textbox", name="Username").fill(login[0]["usrnm"])) # run untill similar to await 
    loop.run_until_complete(page.get_by_role("textbox", name="Password").fill(login[0]["pass"]))
    loop.run_until_complete(page.get_by_role("button", name="Log In").click())
    loop.run_until_complete(asyncio.sleep(3))
    
@then("entre to homepage")
def step_check_url(context):
    page = context.page
    loop = asyncio.get_event_loop()
    loop.run_until_complete(expect(page).to_have_url(url["DEV/HCS"]))
    loop.run_until_complete(context.browser.close())
    loop.run_until_complete(context.playwright_engine.stop())
