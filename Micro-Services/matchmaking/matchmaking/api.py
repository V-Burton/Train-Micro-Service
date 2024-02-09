import httpx

async def remove_channel_name_from_session_api(session_key, channel_name):
    url = 'http://localhost:8006/remove_channel_from_session'
    data = {'session_key': session_key, 'channel_name': channel_name}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
        
        if response.status_code == 200:
            return response.json()  # Renvoie une confirmation ou des détails supplémentaires
        else:
            # Gérer l'erreur
            return None

async def update_user_session_id_api(user_id, session_id):
    url = 'http://localhost:8006/update-session'
    data = {'user_id': user_id, 'session_id': session_id}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
        
        if response.status_code == 201:
            return response.json()
        else:
            return None
