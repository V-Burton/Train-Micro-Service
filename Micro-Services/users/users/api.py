from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import SessionUpdateSerializer
from django.http import JsonResponse
from django.contrib.sessions.models import Session
from .consumers import update_user_session_id  # Supposons que c'est votre fonction de mise à jour

class UpdateSessionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SessionUpdateSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            session_id = serializer.validated_data['session_id']
            
            try:
                user = get_user_model().objects.get(id=user_id)
                update_user_session_id(user, session_id)  # Assurez-vous que cette fonction est asynchrone si nécessaire
                return Response({"message": "Session ID updated successfully"}, status=status.HTTP_200_OK)
            except get_user_model().DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RemoveChannelFromSessionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        session_key = request.data.get('session_key')
        channel_name = request.data.get('channel_name')
        
        try:
            # Récupérer la session Django directement par son clé
            session = Session.objects.get(session_key=session_key)
            session_data = session.get_decoded()
            channel_names = session_data.get("channel_names", [])
            
            if channel_name in channel_names:
                channel_names.remove(channel_name)
                session_data["channel_names"] = channel_names
                session.save()  # Assurez-vous que cette façon de sauvegarder est correcte pour votre configuration
            return Response({"message": "Channel name removed successfully"}, status=status.HTTP_200_OK)
        except Session.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


@api_view(['POST']) #Le decorateur permet de dire a django de parser le json en bibliotheque interpretable facilement en python via request
def update_session(request):
    user_id = request.data.get('user_id')
    session_id = request.data.get('session_id')

    # if not user_id or not session_id:
    #     return Response({"error": "Missing user_id or session_id"}, status=status.HTTP_400_BAD_REQUEST)

    # try:
    #     # Supposons que vous ayez une méthode pour récupérer votre objet utilisateur par ID
    #     user = User.objects.get(pk=user_id)
    # except User.DoesNotExist:
    #     return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # # Appeler votre logique métier pour mettre à jour la session de l'utilisateur
    update_user_session_id(user_id, session_id)

    return JsonResponse({"message": "User session updated successfully"}, status=201)