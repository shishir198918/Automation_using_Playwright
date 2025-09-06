import asyncio
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
            context.in_progress=response_json["cards"]["unassigned"]
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

@given("login into enviroment as per directed")
def listen_him_dashboard(context):
    prepare_him_listener(context)  # Step 1: define the function
    context.loop.run_until_complete(attach_listener_to_page(context))

    

@when("Goto Him_dashboard where list of episode is shown")
def goto_HIM_api(context):
    context.loop.run_until_complete(context.page.get_by_role("link", name="Code Workflow").click())
    context.loop.run_until_complete(context.page.get_by_role("link", name="HIM Workspace").click())
    context.loop.run_until_complete(asyncio.sleep(5))

@then("Match value with UI to API")
def check_api_with_UI(context):
    context.loop.run_until_complete(expect(context.page.get_by_text("Total Episodes:")).to_have_text(f"{context.total_episode}"))
    context.loop.run_until_complete(asyncio.sleep(3))


    



