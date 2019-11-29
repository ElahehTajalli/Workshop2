from django.http import JsonResponse
from message.serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class conversation(APIView):
    def get(self, request):
        s = ConversationSerializer(
            Conversation.objects.all(),
            many=True
        )
        return JsonResponse({
            'conversations': s.data
        })

    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({
                'message': 'Send login request'
            }, status=401)
        else:
            c = addConversationSerializer(data=request.data, context={'user': request.user})
            if c.is_valid():
                c.save()
                return Response("your conversation is created!")

            else:
                return Response({
                    'errors': c.errors
                }, status=status.HTTP_400_BAD_REQUEST)


class message_view(APIView):
    def get(self, request):
        s = GetMessageSerializer(data=request.GET)
        if s.is_valid():
            c = Conversation.objects.get(
                id=request.GET['conversation']
            )
            messages = Messages.objects.filter(
                conversation=c
            )
            s = MessageSerializer(messages, many=True)
            return Response(s.data)
        else:
            return Response(
                s.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({
                'message': 'Send login request'
            }, status=401)
        else:
            s = AddMessageSerializer(
                data=request.data,
                context={
                    'user': request.user
                })
            if s.is_valid():
                s.save()
                r = {
                    'message': 'Your message saved!'
                }
                return Response(r)
            else:
                return Response({
                    'errors': s.errors
                }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({
                'message': 'Send login request'
            }, status=401)
        else:
            n = Messages.objects.filter(id=request.data['id'], sender=request.user)
            if n:
                s = UpdateMessageSerializer(
                    instance=Messages.objects.get(id=request.data['id']),
                    data=request.data,

                )
                if s.is_valid():
                    s.save()
                    return Response(
                        {"message": "Your message updated successfully"}
                    )
                else:
                    return Response({"errors": s.errors})
            else:
                return Response(
                    {"message": "You're not allowed to edit other messages or This message doesn't exist!"}
                )