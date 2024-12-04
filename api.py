from fastapi import FastAPI, Request, Response, status, BackgroundTasks

from fordefi_rest_client import FordefiRestClient
import routes
from secrets_client import RequiredSecrets, SecretsClient
import utils


HYPERNATIVE_FORDEFI_TRANSACTION_ID_HEADER = "Fordefi-Transaction-Id"


utils.initialize_stdout_logger(enable_debug_logging=True)
access_token = SecretsClient(secrets_path="/dev/webhooks-server", aws_region="ap-northeast-1").get_secret(RequiredSecrets.ACCESS_TOKEN)
fordefi_rest_client = FordefiRestClient(access_token=access_token)
app = FastAPI()



"""
{"id":"c3fc507a-bb08-49f3-bcd5-ad7caf87eec0","data":"{\"riskInsight\":{\"id\":\"000000000000\",\"chain\":\"ethereum\",\"name\":\"TEST MESSAGE\",\"category\":\"Technical\",\"timestamp\":\"2024-01-01T00:00:00Z\",\"severity\":\"Medium\",\"details\":\"Message delivered successfully\",\"involvedAssets\":[{\"address\":\"0x6b175474e89094c44da98b954eedeac495271d0f\",\"alias\":\"Maker: Dai Stablecoin\",\"type\":\"Contract\",\"chain\":\"ethereum\"}],\"riskTypeId\":\"T-9999\",\"riskTypeDescription\":\"TEST MESSAGE FOR TESTING CHANNELS\",\"txnHash\":\"0x0000000000000000000000000000000000000000000000000000000000000000\"},\"watchlists\":[{\"id\":0,\"name\":\"TEST WATCHLIST\"}],\"customAgents\":[],\"triggeredAssets\":[],\"securitySuits\":[]}","digitalSignature":"MEUCIQDIM5YpaRZYifD4tDMdvUsOF1RTNkGiGDRDG/57/c32CwIgb/+f1RnI/js9LjvaVGKPHFJqlEW6yDTQaWpTRyoD2S8="}
"""

"""

"""

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