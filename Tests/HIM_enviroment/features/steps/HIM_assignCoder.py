import asyncio
import re
import time

from behave import given, when, then
from playwright.async_api import expect

def extract_name(url):
    for index in range(len(url)-1,0,-1):
        if url[index]=="/":
            return url[index+1:]

 


async def check_api_codeWorkflowMrnsearchRecommendation(req,context):
    req_name = extract_name(req.url)
    if req_name == "codeWorkflowMrnsearchRecommendation":
        response= await req.response()
        if response.ok:
            response_json= await response.json()
            context.total_episode=f"""Total Episodes: {response_json["meta"]["meta"]["total_episodes"]}"""
            context.uncoded=response_json["cards"]["uncoded"]
            context.unassigned=response_json["cards"]["unassigned"]
            context.in_progress=response_json["cards"]["in_progress"]
        else:
            context.failed_api= f"API failed: {response.status} {response.status_txt}"   
    
    if req_name == "him_dashboard_get_filters_coding_manager_screen_users?page_number=1":
        response = await req.response()
        if response.ok:
            response_json= await response.json()
            context.user= response_json["queues"]["user"]
        else:
            context.failed_api= f"API failed: {response.status} {response.status_txt}"   

def prepare_him_listener(context):
    def sync_listener(req):
        # Fire-and-forget coroutine that stores values in context
        context.loop.create_task(check_api_codeWorkflowMrnsearchRecommendation(req, context))

    # Save listener reference in context so you can attach/detach as needed
    context._him_api_listener = sync_listener 

async def attach_listener_to_page(context):
    context.page.on("request", context._him_api_listener)       

@given("Login into environment go to HIM dashboard")
def listen_him_dashboard(context):
    prepare_him_listener(context)  # Step 1: define the function
    context.loop.run_until_complete(attach_listener_to_page(context))

# @when("Into HIM dashboard go to {assign_coder} selecting")
# def goto_HIM_api(context, assign_coder):
#     context.loop.run_until_complete(context.page.locator('a[href="/Code-Workflow"]').click())
#     context.loop.run_until_complete(context.page.get_by_role("link", name="HIM Workspace").click())
#     context.loop.run_until_complete(asyncio.sleep(4))
#     context.loop.run_until_complete(context.page.get_by_role("button", name="Assigned Coder").click())

#     import time
#     waited = 0
#     while not hasattr(context, "user") and waited < 5:
#         time.sleep(1)
#         waited += 1

#     if not hasattr(context, "user"):
#         raise Exception("context.user was not set - API likely not triggered")


#     for user in context.user:
#         if user["user_name"].lower() == assign_coder.lower():  # case-insensitive match
#             checkbox = context.page.locator("div").filter(has_text=re.compile(rf"^{user['user_name']}$")).get_by_role("checkbox")
#             context.loop.run_until_complete(checkbox.check()).click()
#             #time.sleep(4)
#             context.loop.run_until_complete(asyncio.sleep(4))
#             context.loop.run_until_complete(checkbox.uncheck()).click()
#             context.loop.run_until_complete(asyncio.sleep(4))



# @when("Into HIM dashboard go to {assign_coder} selecting")
# def goto_HIM_api(context, assign_coder):
#     context.loop.run_until_complete(context.page.locator('a[href="/Code-Workflow"]').click())
#     context.loop.run_until_complete(context.page.get_by_role("link", name="HIM Workspace").click())
#     context.loop.run_until_complete(asyncio.sleep(4))
#     context.loop.run_until_complete(context.page.get_by_role("button", name="Assigned Coder").click())

#     # Wait until user list is loaded
#     waited = 0
#     while not hasattr(context, "user") and waited < 5:
#         time.sleep(1)
#         waited += 1
#     if not hasattr(context, "user"):
#         raise Exception("context.user was not set - API likely not triggered")

#     # Dynamically find index of the user
#     index = None
#     for idx, user in enumerate(context.user):
#         if user["user_name"].lower() == assign_coder.lower():
#             index = idx
#             break

#     if index is None:
#         raise Exception(f"User '{assign_coder}' not found in context.user list")

#     nth_child = index + 1  # nth-child is 1-based

#     # Optional: Click label with user's name (useful for visibility/debug)
#     context.loop.run_until_complete(context.page.locator("label").filter(has_text=assign_coder).click())

#     # Select and unselect the checkbox using nth-child
#     checkbox_selector = f"div:nth-child({nth_child}) > .form-check-input"
#     checkbox = context.page.locator(checkbox_selector)
#     context.loop.run_until_complete(checkbox.check())
#     context.loop.run_until_complete(asyncio.sleep(1))
#     context.loop.run_until_complete(checkbox.uncheck())
#     context.loop.run_until_complete(asyncio.sleep(2))


@when("Into HIM dashboard go to {assign_coder} selecting")
def goto_HIM_api(context, assign_coder):
    context.loop.run_until_complete(context.page.locator('a[href="/Code-Workflow"]').click())
    context.loop.run_until_complete(context.page.get_by_role("link", name="HIM Workspace").click())
    context.loop.run_until_complete(asyncio.sleep(4))

    # Click the "Assigned Coder" dropdown (which shows the checkboxes)
    context.loop.run_until_complete(context.page.get_by_role("button", name="Assigned Coder").click())

    # Optional: wait a bit for the UI to fully render
    context.loop.run_until_complete(asyncio.sleep(1))

    # Click the coder's label (for visibility or interaction purposes)
    context.loop.run_until_complete(context.page.locator("label").filter(has_text=assign_coder).click())

    # Derive nth-child index manually — assuming consistent structure/order
    # Example: coder list order matches the Examples table or known UI list
    coder_index_map = {
        "sagar": 1,
        "amrutha": 2,
        "unassigned": 11  # <-- Adjust this based on actual DOM inspection
    }

    nth_child = coder_index_map.get(assign_coder.lower())
    if not nth_child:
        raise Exception(f"No known nth-child mapping for coder '{assign_coder}'")

    checkbox_selector = f"div:nth-child({nth_child}) > .form-check-input"
    checkbox = context.page.locator(checkbox_selector)

    context.loop.run_until_complete(checkbox.check())
    context.loop.run_until_complete(asyncio.sleep(3))
    context.loop.run_until_complete(checkbox.uncheck())
    context.loop.run_until_complete(asyncio.sleep(3))


@then("validate data with API with element Total Episode, Uncoded, Unassigned and In progress")
def check_api_with_UI(context):
    context.loop.run_until_complete(expect(context.page.get_by_text("Total Episodes:")).to_have_text(f"{context.total_episode}"))
    context.loop.run_until_complete(asyncio.sleep(3))
