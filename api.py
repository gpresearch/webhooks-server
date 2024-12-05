from fastapi import FastAPI, Request, Response, status, BackgroundTasks

from fordefi_rest_client import FordefiRestClient
import routes
from secrets_client import RequiredSecrets, SecretsClient
import utils
from pymetrics import MetricsWriter, init_rust_logging


HYPERNATIVE_FORDEFI_TRANSACTION_ID_HEADER = "Fordefi-Transaction-Id"


utils.initialize_stdout_logger(enable_debug_logging=True)
access_token = SecretsClient(secrets_path="/prod/webhooks-server", aws_region="ap-northeast-1").get_secret(RequiredSecrets.FORDEFI_ACCESS_TOKEN)
init_rust_logging()
metrics_client = MetricsWriter.new_influx(
    influx_url="http://localhost:8086",
    database="dev",
    namespace="webhooks-server.main",
)
fordefi_rest_client = FordefiRestClient(access_token=access_token, metrics_client=metrics_client)

app = FastAPI()



@app.get("/")
async def root():
    return {"message": "Hello World"}

"""
ca123350-61ff-424a-9bd9-8a951c3d9d09
"""
@app.post("/fordefi_webhook")
async def fordefi_webhook(request : Request, background_tasks: BackgroundTasks):
    # Extract Fordefi-Transaction-Id header.
    fordefi_transaction_id = request.headers.get(HYPERNATIVE_FORDEFI_TRANSACTION_ID_HEADER)
    background_tasks.add_task(routes.handle_fordefi_webhook, fordefi_rest_client,fordefi_transaction_id)
    return Response(status_code=status.HTTP_200_OK)


@app.get("/get_tx")
async def get_tx(request : Request, background_tasks: BackgroundTasks):
    # Extract Fordefi-Transaction-Id header.
    fordefi_transaction_id = request.headers.get(HYPERNATIVE_FORDEFI_TRANSACTION_ID_HEADER)
    background_tasks.add_task(routes.get_tx_fordefi, fordefi_rest_client,fordefi_transaction_id)
    return Response(status_code=status.HTTP_200_OK)