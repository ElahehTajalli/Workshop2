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
        c = addConversationSerializer(data=request.data)
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
        print(request.data)
        s = UpdateMessageSerializer(
            instance=Messages.objects.get(id=request.data['id']),
            data=request.data,

        )
        if s.is_valid():
            s.save()
            return Response(
                {
                    "message": "Your message updated successfully"
                }
            )
        else:
            return Response(
                {
                    "errors": s.errors
                }
            )