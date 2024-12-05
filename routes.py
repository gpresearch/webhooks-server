"""
Route handlers for the API.
"""

from fordefi_rest_client import FordefiRestClient



async def handle_fordefi_webhook(fordefi_rest_client : FordefiRestClient, fordefi_id : str):
    """
    Handle the fordefi webhook request from Hypernative.
    """

    # Make request to Fordefi API.
    await fordefi_rest_client.trigger_transaction_signing(fordefi_id)
    
    # Record a metric.
    pass

async def get_tx_fordefi(fordefi_rest_client : FordefiRestClient, fordefi_id : str):
    """
    Handle the fordefi webhook request from Hypernative.
    """

    # Make request to Fordefi API.
    await fordefi_rest_client.get_transaction(fordefi_id)
    
    # Record a metric.
    pass

