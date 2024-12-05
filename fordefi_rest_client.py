

import aiohttp
from utils import logger
from pymetrics import MetricsWriter

class FordefiRestClient:

    DEFAULT_BASE_URL = "https://api.fordefi.com/"

    def __init__(self, access_token : str, metrics_client : MetricsWriter, base_url: str = DEFAULT_BASE_URL):
        self.base_url = base_url
        self.access_token = access_token
        self.metrics_client = metrics_client
        self.session = aiohttp.ClientSession()

    async def trigger_transaction_signing(self, tx_id : str):
        """
        https://api.fordefi.com/redoc#tag/Transactions/operation/trigger_transaction_signing_api_v1_transactions__id__trigger_signing_post
        """
        endpoint = f"api/v1/transactions/{tx_id}/trigger-signing"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }

        logger.info(f"starting rest request to {self.base_url}")
        async with self.session.post(url=self.base_url+endpoint,headers=headers) as resp:
            # self.metrics_client.record_event(name="trigger_transaction_signing", time=1_000_000, tags={"status_code": resp.status})
            status_code = resp.status

            if status_code != 204:
                logger.error(f"API request failed with status code {status_code}: {await resp.text()}")
                return

            logger.info(f"API request succeeded: {await resp.json()}")


    async def get_transaction(self, tx_id : str):
        """
        https://api.fordefi.com/redoc#tag/Transactions/operation/trigger_transaction_signing_api_v1_transactions__id__trigger_signing_post
        """
        endpoint = f"api/v1/transactions/{tx_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }

        logger.info(f"starting rest request to {self.base_url}")
        async with self.session.get(url=self.base_url+endpoint,headers=headers) as resp:
            status_code = resp.status
            # self.metrics_client.record_event(name="trigger_transaction_signing")
            # self.metrics_client.record_latency(name="trigger_transaction_signing",took_ns=1_000_000)

            if status_code != 20:
                logger.error(f"API request failed with status code {status_code}: {await resp.text()}")
                return

            logger.info(f"API request succeeded: {await resp.json()}")
    



if __name__ == "__main__":
    pass