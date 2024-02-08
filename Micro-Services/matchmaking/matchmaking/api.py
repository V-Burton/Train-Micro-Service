import httpx

async def create_game_instance(id):
    url = 'http://localhost:8003/create_game_instance'
    data = {"session_id": id}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
        if response.status_code == 200:
            print("Channel name removed successfully")
        else:
            print("Failed to remove channel name")