import time
import uuid
import json

from .pong import session as session
from .pong import constants as g
import logging

import jwt
from django.http import QueryDict
from django.http import HttpResponse
from . import settings

logger = logging.getLogger(__name__)

from django.http import JsonResponse, StreamingHttpResponse

def game_create_view(request):
    # Check the HTTP method
    if request.method != "POST":
        response = JsonResponse({"error": "Invalid HTTP method: POST required"}, status=405)
        response["Allow"] = "POST"
        return response

    # Verify that the client has an username
    # username = request.session.get("username")
    user_id = getattr(request, 'user_id', None)
    logger.error('user_id1 =', user_id)
    if user_id is None:
        return JsonResponse({"error": "Please pick an user_id first1"}, status=400)

    # Check for an active game session for this user or a game session waiting for a second player
    has_session, waiting_game = session.session_has(user_id), session.session_waiting(user_id)
    if has_session or waiting_game:
        data = session.session_get_state(has_session) if has_session else session.session_get_state(waiting_game)
        return JsonResponse({"id": data["id"]}, status=200)

    # Create a new game
    game_id = uuid.uuid4()
    session.session_create(game_id, user_id)
    return JsonResponse({"id": game_id}, status=201)


def game_view(request, game_id: uuid.UUID):
##################################################################
    token = get_token_from_request(request)
    logger.error("let's see this token", token)
    if token:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            # Utilisez les informations du payload comme nécessaire
            # Par exemple : user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return HttpResponse('Token has expired', status=401)
        except jwt.InvalidTokenError:
            return HttpResponse('Invalid token', status=401)
        # Générez votre réponse SSE ici
    else:
        logger.error("occurs here")
        return HttpResponse('Token is required', status=400)
###################################################################  
    # Verify that the client has an user_id
    # user_id = request.session.get("user_id")
    request.user_id = payload.get('user_id')
    user_id = getattr(request, 'user_id', None)
    logger.error('user_id2 =', user_id)
    if user_id is None:
        return JsonResponse({"error": "Please pick an username first2"}, status=400)

    # Check that the game exists
    if not session.session_exists(game_id):
        return JsonResponse({"error": "Invalid game ID"}, status=403)

    # Check that the client is part of that game
    if not session.session_is_in(game_id, user_id):
        return JsonResponse({"error": "You are not part of this game"}, status=403)

    # Handle PUT request for updating game state
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            # Ensure data is a list with two elements
            if not (isinstance(data, list) and len(data) == 2):
                raise ValueError("Input must be a pair of [input, timestamp]")
        except (json.JSONDecodeError, ValueError) as e:
            return JsonResponse({"error": str(e)}, status=400)

        input, timestamp = data
        if input not in g.INPUTS:
            return JsonResponse({"error": "Invalid value for 'input'"}, status=400)

        session.session_add_input(game_id, user_id, input, timestamp)
        return JsonResponse({}, status=200)

    # Handle GET request for streaming game state
    elif request.method == "GET":
        # FIXME Should this be async ?
        def event_stream():
            sleep_time = 1 / 10
            while True:
                try:
                    session.session_update(game_id)
                    data = session.session_get_state_small(game_id)
                    yield f"data: {json.dumps(data)}\n\n".encode("utf-8")
                    time.sleep(sleep_time)
                except GeneratorExit:
                    break
                except Exception as e:
                    yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n".encode("utf-8")
                    break

        response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
        response["Cache-Control"] = "no-cache"
        return response

    else:
        response = JsonResponse({"error": "Invalid HTTP method: GET or PUT required"}, status=405)
        response["Allow"] = "GET, PUT"
        return response
    

import json

def get_token_from_request(request):
    token = request.GET.get('token')
    
    if token:
        return token
    
    if request.method in ['POST', 'PUT']:
        # Tentez de lire le corps de la requête comme JSON
        try:
            body = json.loads(request.body.decode('utf-8'))  # Assurez-vous de décoder le corps de la requête
            # Gérez le cas où le corps est un dictionnaire
            if isinstance(body, dict):
                token = body.get('token')
            # Gérez le cas où le corps est une liste
            elif isinstance(body, list):
                # Vous pouvez ajuster cette logique en fonction de la structure attendue de votre liste
                for item in body:
                    if isinstance(item, dict) and 'token' in item:
                        token = item.get('token')
                        break
        except json.JSONDecodeError:
            pass
    
    if not token:
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token.split(' ')[1]
    
    return token
