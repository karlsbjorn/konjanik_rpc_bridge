import json
import os

import websockets
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import APIKeyHeader


X_API_KEY = APIKeyHeader(name="X-API-Key")


def api_key_auth(x_api_key: str = Depends(X_API_KEY)):
    if x_api_key != os.environ["API_KEY"]:
        raise HTTPException(status_code=401, detail="No")


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


app = FastAPI(title="Konjanik API", openapi_url="/konjanik/openapi.json")


@app.get("/konjanik/get-current-track", dependencies=[Depends(api_key_auth)])
async def get_current_track(guild_id: int):
    result = (
        await rpc_call(
            "PYLAVRPC__GET_CURRENT_TRACK",
            [
                guild_id,
            ],
        )
    ).get("result")
    if (status := result.get("status")) and status != 200:
        raise HTTPException(status_code=result, detail=result)
    return result


@app.post("/konjanik/play-track", dependencies=[Depends(api_key_auth)])
async def play_track(guild_id: int, query: str):
    result = (
        await rpc_call(
            "PYLAVRPC__PLAY_TRACK",
            [guild_id, query],
        )
    ).get("result")
    if (status := result.get("status")) and status != 200:
        raise HTTPException(status_code=result, detail=result)
    return result


@app.post("/konjanik/play-next-track", dependencies=[Depends(api_key_auth)])
async def play_next_track(guild_id: int):
    result = (
        await rpc_call(
            "PYLAVRPC__PLAY_NEXT",
            [
                guild_id,
            ],
        )
    ).get("result")
    if (status := result.get("status")) and status != 200:
        raise HTTPException(status_code=result, detail=result)
    return result


@app.get("/konjanik/adventure/get-user-profile")
async def get_user_profile(user_id: int):
    result = (
        await rpc_call(
            "PYLAVRPC__PLAY_NEXT",
            [
                user_id,
            ],
        )
    ).get("result")
    if (status := result.get("status")) and status != 200:
        raise HTTPException(status_code=result, detail=result)
    return result
