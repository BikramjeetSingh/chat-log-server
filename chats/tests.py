from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils.functional import cached_property

from chats.models import ChatMessage


class ChatLogListTest(TestCase):

    @cached_property
    def url(self):
        return reverse("chatlog-list", kwargs={'user_id': self.test_user.id})

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(
            username="test",
            email="user@test.com",
            password="test123",
        )

    def test_chat_list_empty(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json, [])

    def test_chat_list_non_empty(self):
        ChatMessage.objects.create(
            user=self.test_user,
            content="foo",
            timestamp=datetime.utcfromtimestamp(1897138827),
            is_sent=True,
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(len(response_json), 1)
        self.assertEqual(response_json[0]['content'], "foo")

    def test_chat_list_limit(self):
        ChatMessage.objects.create(
            user=self.test_user,
            content="msg1",
            timestamp=datetime.utcfromtimestamp(1897138827),  # 12-02-2030
            is_sent=True,
        )
        ChatMessage.objects.create(
            user=self.test_user,
            content="msg2",
            timestamp=datetime.utcfromtimestamp(1581519627),  # 12-02-2020
            is_sent=True,
        )
        ChatMessage.objects.create(
            user=self.test_user,
            content="msg3",
            timestamp=datetime.utcfromtimestamp(2212671627),  # 12-02-2040
            is_sent=True,
        )

        response = self.client.get(f"{self.url}?limit=2")
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(len(response_json), 2)
        self.assertEqual(response_json[0]['content'], "msg3")
        self.assertEqual(response_json[1]['content'], "msg1")

    def test_chat_list_limit_start(self):
        ChatMessage.objects.create(
            user=self.test_user,
            content="msg1",
            timestamp=datetime.utcfromtimestamp(1897138827),  # 12-02-2030
            is_sent=True,
        )
        ChatMessage.objects.create(
            user=self.test_user,
            content="msg2",
            timestamp=datetime.utcfromtimestamp(1581519627),  # 12-02-2020
            is_sent=True,
        )
        ChatMessage.objects.create(
            user=self.test_user,
            content="msg3",
            timestamp=datetime.utcfromtimestamp(2212671627),  # 12-02-2040
            is_sent=True,
        )
        ChatMessage.objects.create(
            user=self.test_user,
            content="msg4",
            timestamp=datetime.utcfromtimestamp(1423753227),  # 12-02-2015
            is_sent=True,
        )

        response = self.client.get(f"{self.url}?limit=2&start=1")
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(len(response_json), 2)
        self.assertEqual(response_json[0]['content'], "msg1")
        self.assertEqual(response_json[1]['content'], "msg2")

    def test_chat_list_limit_start_not_exists(self):
        ChatMessage.objects.create(
            user=self.test_user,
            content="msg1",
            timestamp=datetime.utcfromtimestamp(1897138827),  # 12-02-2030
            is_sent=True,
        )
        ChatMessage.objects.create(
            user=self.test_user,
            content="msg2",
            timestamp=datetime.utcfromtimestamp(1581519627),  # 12-02-2020
            is_sent=True,
        )
        ChatMessage.objects.create(
            user=self.test_user,
            content="msg3",
            timestamp=datetime.utcfromtimestamp(2212671627),  # 12-02-2040
            is_sent=True,
        )
        ChatMessage.objects.create(
            user=self.test_user,
            content="msg4",
            timestamp=datetime.utcfromtimestamp(1423753227),  # 12-02-2015
            is_sent=True,
        )

        response = self.client.get(f"{self.url}?limit=2&start=6")
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertEqual(response_json, {'msg': 'Could not find message with id 6'})


class ChatLogCreateTest(TestCase):

    @cached_property
    def url(self):
        return reverse("chatlog-list", kwargs={'user_id': self.test_user.id})

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(
            username="test",
            email="user@test.com",
            password="test123",
        )

    def test_create_chat_log_missing_parameters(self):
        response = self.client.post(self.url, data={
            'content': 'foo',
            'timestamp': 1897138827,
        })
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertEqual(response_json, {'is_sent': ['This field is required.']})

    def test_create_chat_log_invalid_parameters(self):
        response = self.client.post(self.url, data={
            'content': 'foo',
            'timestamp': 'random',
            'is_sent': True,
        })
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertEqual(response_json, {'timestamp': ['Enter a whole number.']})

    def test_create_chat_log_success(self):
        response = self.client.post(self.url, data={
            'content': 'foo',
            'timestamp': 1897138827,
            'is_sent': True,
        })
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json, {'message_id': 1})
        self.assertTrue(ChatMessage.objects.filter(id=1).exists())


class ChatLogDeleteAllTest(TestCase):

    @cached_property
    def url(self):
        return reverse("chatlog-list", kwargs={'user_id': self.test_user.id})

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(
            username="test",
            email="user@test.com",
            password="test123",
        )

    def test_delete_chat_log(self):
        ChatMessage.objects.create(
            user=self.test_user,
            content="foo",
            timestamp=datetime.utcfromtimestamp(1897138827),
            is_sent=True,
        )

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json, {'msg': 'Successfully deleted all messages for user with id 1'})
        self.assertFalse(ChatMessage.objects.filter(user=self.test_user).exists())


class ChatLogDeleteTest(TestCase):

    @cached_property
    def url(self):
        return reverse("chatlog-detail", kwargs={'user_id': self.test_user.id, 'msg_id': self.test_message.id})

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(
            username="test",
            email="user@test.com",
            password="test123",
        )
        cls.test_message = ChatMessage.objects.create(
            user=cls.test_user,
            content="foo",
            timestamp=datetime.utcfromtimestamp(1897138827),
            is_sent=True,
        )

    def test_delete_chat_log(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json, {'msg': 'Successfully deleted message with id 1'})
        self.assertFalse(ChatMessage.objects.filter(user=self.test_user).exists())
