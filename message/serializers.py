from rest_framework import serializers
from message.models import Conversation, Messages
from user.serializers import UserSerializer


class ConversationSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True)

    class Meta:
        model = Conversation
        fields = '__all__'


class addConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['name', 'members']

    def create(self, validated_data):
        print(type(validated_data['members']))
        c = Conversation(
            name=validated_data['name'],
        )
        c.save()
        c.members.add(self.context['user'])
        for v in validated_data['members']:
            c.members.add(v)
        return c


class UpdateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ["id", "text"]


class GetMessageSerializer(serializers.Serializer):
    conversation = serializers.IntegerField()


class AddMessageSerializer(serializers.Serializer):
    conversation = serializers.IntegerField()
    text = serializers.CharField(
        max_length=100,
        allow_blank=False)

    def create(self, validated_data):
        c = Conversation.objects.get(
            id=validated_data['conversation'])
        m = Messages(
            text=validated_data['text'],
            sender=self.context['user'],
            conversation=c
        )
        print(m.sender)
        m.save()
        return m


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()

    class Meta:
        model = Messages
        fields = '__all__'