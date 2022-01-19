import json
from datetime import datetime
from typing import List, Dict

from django import views
from django.contrib.auth.models import User
from django.http import HttpResponse

from chats.forms import ChatLogForm
from chats.models import ChatMessage


class ChatLogListView(views.View):

    @staticmethod
    def _get_index_of_object_in_list(obj_id: int, obj_list: List) -> int:
        for index, obj in enumerate(obj_list):
            if obj['id'] == obj_id:
                return index
        raise IndexError

    def _get_chat_messages_for_user(self, user: User, limit: int, start_id: int = 0) -> List[Dict]:
        """
        For a particular user, returns a list of ChatMessage objects in descending order of timestamp (i.e most
        recent messages appear first).

        :param user: The user whose messages need to be retrieved
        :param limit: The number of messages to be fetched.
        :param start_id: The id of the message from where to start counting.

        :return: a list of dictionaries containing the required chat messages, in the format ...
        [{
            "id": 1,
            "user_id": 1,
            "content": "some message content",
            "timestamp": "2020-02-12 15:00:27+00:00"
            "is_sent": True,
        }]
        """
        chat_messages = list(ChatMessage.objects.filter(user=user).order_by('-timestamp').values())
        if start_id != 0:
            start_index = self._get_index_of_object_in_list(start_id, chat_messages)
            chat_messages = chat_messages[start_index:]
        return chat_messages[:limit]

    def get(self, request, user_id, *args, **kwargs):
        limit = int(request.GET.get('limit', 10))
        start = int(request.GET.get('start', 0))

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return HttpResponse(
                status=404,
                content_type="application/json",
                content=json.dumps({
                    "msg": f"Could not find user with id {user_id}"
                }),
            )

        try:
            chat_messages = self._get_chat_messages_for_user(user, limit, start)
        except IndexError:
            return HttpResponse(
                status=400,
                content_type="application/json",
                content=json.dumps({
                    "msg": f"Could not find message with id {start}"
                }),
            )

        return HttpResponse(
            status=200,
            content_type="application/json",
            content=json.dumps(chat_messages, default=str),
        )

    def post(self, request, user_id, *args, **kwargs):
        user = User.objects.get(id=user_id)
        form = ChatLogForm(data=request.POST)

        if not form.is_valid():
            return HttpResponse(
                status=400,
                content_type="application/json",
                content=json.dumps(form.errors),
            )

        chat_message = ChatMessage.objects.create(
            user=user,
            content=form.cleaned_data['content'],
            timestamp=datetime.utcfromtimestamp(  # Convert the Unix timestamp into a Python datetime object
                form.cleaned_data['timestamp']
            ),
            is_sent=form.cleaned_data['is_sent'],
        )

        return HttpResponse(
            status=200,
            content_type="application/json",
            content=json.dumps({
                'message_id': chat_message.id,
            }),
        )

    def delete(self, request, user_id, *args, **kwargs):
        user = User.objects.get(id=user_id)
        ChatMessage.objects.filter(user=user).delete()

        return HttpResponse(
            status=200,
            content_type="application/json",
            content=json.dumps({
                'msg': f'Successfully deleted all messages for user with id {user_id}',
            }),
        )


class ChatLogDetailView(views.View):

    def delete(self, request, user_id, msg_id, *args, **kwargs):
        try:
            ChatMessage.objects.get(user__id=user_id, id=msg_id).delete()
            return HttpResponse(
                status=200,
                content_type="application/json",
                content=json.dumps({
                    'msg': f'Successfully deleted message with id {msg_id}',
                }),
            )
        except ChatMessage.DoesNotExist:
            return HttpResponse(
                status=404,
                content_type="application/json",
                content=json.dumps({
                    'msg': f"Could not find message with id {msg_id}",
                }),
            )

