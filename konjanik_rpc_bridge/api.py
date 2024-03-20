import json

import websockets
from fastapi import FastAPI


async def rpc_call(method: str, params: list) -> dict:
    """Calls an RPC method registered on the bot

    :param method: Name of the method to call. This must be registered on the bot first.
    :param params: The args
    :return: The return of the RPC call converted to a dict
    """
    async with websockets.connect("ws://127.0.0.1:6133") as websocket:
        request_data = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
        await websocket.send(json.dumps(request_data))
        response = await websocket.recv()
        return json.loads(response)


app = FastAPI(openapi_url="/konjanik/openapi.json")


@app.get("/konjanik/get-current-track")
async def get_current_track(guild_id: int):
    return (
        await rpc_call(
            "KONJANIKTOOLS__GET_CURRENT_TRACK",
            [
                guild_id,
            ],
        )
    ).get("result")
