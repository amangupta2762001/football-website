from app import create_app
from serverless_wsgi import handle_request

app = create_app()

def handler(event, context):
    return handle_request(app, event, context)