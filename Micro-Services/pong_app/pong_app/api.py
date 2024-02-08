import httpx


async def GameSession_api(id):
    url = 'http://localhost:8003/create_game_instance'
    data = {"session_id": id}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
        if response.status_code == 200:
            print("Channel name removed successfully")
        else:
            print("Failed to remove channel name")

async def remove_channel_name_from_session_api(scope, channel_name):
    url = 'http://localhoste:8002/GameSession'
    data = {"scope": scope, "channel_name": channel_name}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
        if response.status_code == 200:
            print("Channel name removed successfully")
        else:
            print("Failed to remove channel name")


async def add_channel_name_to_session_api(scope, channel_name):
    url = 'http://localhoste:8002/GameSession'
    data = {"scope": session_id, "channel_name": channel_name}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
        if response.status_code == 200:
            print("Channel name removed successfully")
        else:
            print("Failed to remove channel name")
