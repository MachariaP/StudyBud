import asyncio
import json

from django.test import TestCase, Client
from django.contrib.auth.models import User, AnonymousUser
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async

from .models import Topic, Room, Message, Profile
from .forms import UserForm, ProfileForm
from .consumers import ChatConsumer


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.topic = Topic.objects.create(name='Python')
        self.room = Room.objects.create(
            host=self.user,
            topic=self.topic,
            name='Test Room',
            description='A test room'
        )
        self.message = Message.objects.create(
            user=self.user,
            room=self.room,
            body='Test message'
        )

    def test_topic_creation(self):
        self.assertEqual(self.topic.name, 'Python')
        self.assertEqual(str(self.topic), 'Python')

    def test_room_creation(self):
        self.assertEqual(self.room.name, 'Test Room')
        self.assertEqual(self.room.host, self.user)
        self.assertEqual(self.room.topic, self.topic)
        self.assertIn(self.room.description, 'A test room')
        self.assertEqual(str(self.room), 'Test Room')

    def test_room_ordering(self):
        room2 = Room.objects.create(
            host=self.user,
            topic=self.topic,
            name='Newer Room'
        )
        rooms = Room.objects.all()
        self.assertEqual(rooms[0], room2)

    def test_message_creation(self):
        self.assertEqual(self.message.body, 'Test message')
        self.assertEqual(self.message.user, self.user)
        self.assertEqual(self.message.room, self.room)
        self.assertEqual(str(self.message), 'Test message')

    def test_profile_created_on_user_creation(self):
        """A Profile should be auto-created when a User is created."""
        new_user = User.objects.create_user(
            username='janedoe', password='testpass123'
        )
        self.assertTrue(Profile.objects.filter(user=new_user).exists())
        self.assertEqual(new_user.profile.bio, '')
        self.assertFalse(new_user.profile.avatar)

    def test_profile_str(self):
        """Profile string representation should include the username."""
        self.assertEqual(str(self.user.profile), "testuser's profile")

    def test_profile_bio_update(self):
        """Updating the bio via the Profile model should persist."""
        self.user.profile.bio = 'Hello, I love Python!'
        self.user.profile.save()
        updated = Profile.objects.get(user=self.user)
        self.assertEqual(updated.bio, 'Hello, I love Python!')


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.topic = Topic.objects.create(name='Django')
        self.room = Room.objects.create(
            host=self.user,
            topic=self.topic,
            name='Django Room'
        )

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/home.html')

    def test_home_page_search(self):
        response = self.client.get('/?q=Django')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Room')

    def test_room_page(self):
        response = self.client.get(f'/room/{self.room.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/room.html')
        self.assertContains(response, 'Django Room')

    def test_room_page_404(self):
        response = self.client.get('/room/999/')
        self.assertEqual(response.status_code, 404)

    def test_login_page(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/login_register.html')

    def test_login(self):
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertRedirects(response, '/')

    def test_login_failure(self):
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Username or password')

    def test_register_page(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/logout/')
        self.assertRedirects(response, '/')

    def test_profile_page(self):
        response = self.client.get(f'/profile/{self.user.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/profile.html')

    def test_create_room_requires_login(self):
        response = self.client.get('/create-room/')
        self.assertRedirects(response, '/login/?next=/create-room/')

    def test_create_room(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post('/create-room/', {
            'topic': 'JavaScript',
            'name': 'JS Room',
            'description': 'Chat about JS'
        })
        self.assertRedirects(response, '/')
        self.assertTrue(Room.objects.filter(name='JS Room').exists())

    def test_update_room_requires_login(self):
        response = self.client.get(f'/update-room/{self.room.id}/')
        self.assertRedirects(response, f'/login/?next=/update-room/{self.room.id}/')

    def test_delete_room_requires_login(self):
        response = self.client.get(f'/delete-room/{self.room.id}/')
        self.assertRedirects(response, f'/login/?next=/delete-room/{self.room.id}/')

    def test_topics_page(self):
        response = self.client.get('/topics/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/topics.html')
        self.assertContains(response, 'Django')

    def test_topics_search(self):
        response = self.client.get('/topics/?q=Python')
        self.assertEqual(response.status_code, 200)

    def test_update_user_requires_login(self):
        response = self.client.get('/update-user/')
        self.assertRedirects(response, '/login/?next=/update-user/')

    def test_post_message_in_room(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(f'/room/{self.room.id}/', {
            'body': 'Hello from test'
        })
        self.assertRedirects(response, f'/room/{self.room.id}/')
        self.assertTrue(Message.objects.filter(body='Hello from test').exists())

    def test_update_user_bio_and_avatar(self):
        """Submitting the update-user form should save bio."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post('/update-user/', {
            'username': 'testuser',
            'email': '',

            'bio': 'I love Django!',
        })
        self.assertRedirects(response, f'/profile/{self.user.id}/')
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.bio, 'I love Django!')

    def test_profile_page_shows_bio(self):
        """The profile page should display the user's bio."""
        self.user.profile.bio = 'Django enthusiast'
        self.user.profile.save()
        response = self.client.get(f'/profile/{self.user.id}/')
        self.assertContains(response, 'Django enthusiast')

    def test_profile_page_shows_stats(self):
        """The profile page should display room/message counts."""
        self.client.login(username='testuser', password='testpass123')
        self.client.post(f'/room/{self.room.id}/', {'body': 'Hello!'})
        response = self.client.get(f'/profile/{self.user.id}/')
        self.assertContains(response, 'Rooms')
        self.assertContains(response, 'Messages')

    def test_register_creates_profile(self):
        """Registering a new user should auto-create their Profile."""
        self.client.login(username='testuser', password='testpass123')
        # Just verify the existing user already has a profile from the signal
        self.assertTrue(Profile.objects.filter(user=self.user).exists())
        self.assertEqual(self.user.profile.bio, '')
        self.assertFalse(self.user.profile.avatar)

    def test_profile_form_valid(self):
        """ProfileForm should be valid with bio data."""
        form = ProfileForm(data={'bio': 'Test bio'})
        self.assertTrue(form.is_valid())

    def test_forgot_password_page(self):
        """Forgot password page should render correctly."""
        response = self.client.get('/forgot-password/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/forgot_password.html')

    def test_forgot_password_post(self):
        """Submitting forgot password should redirect with success message."""
        response = self.client.post('/forgot-password/', {'email': 'test@example.com'})
        self.assertRedirects(response, '/login/')

    def test_forgot_password_with_valid_user_email(self):
        """Submitting with a real user email should still redirect with success."""
        self.user.email = 'testuser@example.com'
        self.user.save()
        response = self.client.post('/forgot-password/', {'email': 'testuser@example.com'})
        self.assertRedirects(response, '/login/')

    def test_reset_password_page_invalid_token(self):
        """Invalid reset token should redirect to forgot-password with error."""
        response = self.client.get('/reset/invalid-token/more-invalid/')
        self.assertRedirects(response, '/forgot-password/')


class WebSocketConsumerTests(TestCase):
    """Tests for the ChatConsumer WebSocket implementation."""

    def setUp(self):
        """Create test users, topic, and room for consumer tests."""
        self.user = User.objects.create_user(
            username='alice', password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='bob', password='testpass123'
        )
        self.topic = Topic.objects.create(name='Python')
        self.room = Room.objects.create(
            host=self.user,
            topic=self.topic,
            name='Test Chat Room',
        )

    async def _build_communicator(self, user=None):
        """Build a WebsocketCommunicator for the ChatConsumer.

        Args:
            user: Authenticated User or AnonymousUser. Defaults to self.user.

        Returns:
            A configured WebsocketCommunicator instance.
        """
        if user is None:
            user = self.user
        communicator = WebsocketCommunicator(
            ChatConsumer.as_asgi(),
            f'/ws/chat/{self.room.id}/',
        )
        communicator.scope['user'] = user
        communicator.scope['url_route'] = {
            'kwargs': {'room_id': str(self.room.id)},
        }
        return communicator

    async def test_connect_authenticated(self):
        """An authenticated user should successfully connect."""
        comm = await self._build_communicator()
        connected, _ = await comm.connect()
        self.assertTrue(connected)
        await comm.disconnect()

    async def test_connect_unauthenticated_rejected(self):
        """An unauthenticated user should be rejected with code 4000."""
        anon = AnonymousUser()
        comm = await self._build_communicator(user=anon)
        connected, _ = await comm.connect()
        self.assertFalse(connected)

    async def test_connect_invalid_room_rejected(self):
        """Connecting with a non-existent room ID should be rejected."""
        comm = WebsocketCommunicator(
            ChatConsumer.as_asgi(),
            '/ws/chat/99999/',
        )
        comm.scope['user'] = self.user
        comm.scope['url_route'] = {
            'kwargs': {'room_id': '99999'},
        }
        connected, _ = await comm.connect()
        self.assertFalse(connected)

    async def test_send_and_receive_message(self):
        """Sending a message should save it to DB and broadcast to the group."""
        comm = await self._build_communicator()
        connected, _ = await comm.connect()
        self.assertTrue(connected)

        await comm.send_json_to({
            'type': 'message',
            'body': 'Hello WebSocket!',
        })

        response = await comm.receive_json_from()
        self.assertEqual(response['type'], 'new_message')
        self.assertEqual(response['body'], 'Hello WebSocket!')
        self.assertEqual(response['user'], 'alice')
        self.assertIn('id', response)
        self.assertIn('created', response)

        # Verify message is persisted in DB
        msg = await self._get_message(response['id'])
        self.assertIsNotNone(msg)
        self.assertEqual(msg.body, 'Hello WebSocket!')
        self.assertEqual(msg.user_id, self.user.id)
        self.assertEqual(msg.room_id, self.room.id)

        await comm.disconnect()

    async def test_send_empty_message_ignored(self):
        """Sending an empty or whitespace-only message should not broadcast or persist."""
        comm = await self._build_communicator()
        connected, _ = await comm.connect()
        self.assertTrue(connected)

        msg_count = await self._get_message_count()

        await comm.send_json_to({
            'type': 'message',
            'body': '   ',
        })

        await comm.disconnect()

        final_count = await self._get_message_count()
        self.assertEqual(final_count, msg_count)

    async def test_typing_indicator_broadcast(self):
        """Sending a typing event should broadcast to the group."""
        comm = await self._build_communicator()
        connected, _ = await comm.connect()
        self.assertTrue(connected)

        # Send typing start
        await comm.send_json_to({
            'type': 'typing',
            'typing': True,
        })

        response = await comm.receive_json_from()
        self.assertEqual(response['type'], 'user_typing')
        self.assertEqual(response['user'], 'alice')
        self.assertTrue(response['typing'])

        # Send typing stop
        await comm.send_json_to({
            'type': 'typing',
            'typing': False,
        })

        response = await comm.receive_json_from()
        self.assertEqual(response['type'], 'user_typing')
        self.assertEqual(response['user'], 'alice')
        self.assertFalse(response['typing'])

        await comm.disconnect()

    async def test_avatar_url_in_broadcast(self):
        """A sent message should include avatar_url in the broadcast."""
        comm = await self._build_communicator()
        connected, _ = await comm.connect()
        self.assertTrue(connected)

        await comm.send_json_to({
            'type': 'message',
            'body': 'avatar check',
        })

        response = await comm.receive_json_from()
        self.assertEqual(response['type'], 'new_message')
        self.assertIn('avatar_url', response)
        self.assertIsNone(response['avatar_url'])  # no avatar set

        await comm.disconnect()

    async def test_message_broadcast_to_multiple_clients(self):
        """A message sent by one client should be received by another client in the same room."""
        comm1 = await self._build_communicator()
        connected1, _ = await comm1.connect()
        self.assertTrue(connected1)

        comm2 = await self._build_communicator(user=self.user2)
        connected2, _ = await comm2.connect()
        self.assertTrue(connected2)

        # alice sends a message
        await comm1.send_json_to({
            'type': 'message',
            'body': 'Hey Bob!',
        })

        # Both clients should receive the broadcast
        resp1 = await comm1.receive_json_from()
        resp2 = await comm2.receive_json_from()

        self.assertEqual(resp1['body'], 'Hey Bob!')
        self.assertEqual(resp2['body'], 'Hey Bob!')
        self.assertEqual(resp1['id'], resp2['id'])

        await comm1.disconnect()
        await comm2.disconnect()

    async def test_disconnect_leaves_group(self):
        """After disconnect, a client should no longer receive messages."""
        comm1 = await self._build_communicator()
        connected1, _ = await comm1.connect()
        self.assertTrue(connected1)

        comm2 = await self._build_communicator(user=self.user2)
        connected2, _ = await comm2.connect()
        self.assertTrue(connected2)

        # Disconnect comm2
        await comm2.disconnect()

        # comm1 sends a message
        await comm1.send_json_to({
            'type': 'message',
            'body': 'Only for connected',
        })

        # comm1 receives it
        resp = await comm1.receive_json_from()
        self.assertEqual(resp['body'], 'Only for connected')

        # comm2 should NOT receive it (already disconnected)
        with self.assertRaises(Exception):
            await comm2.receive_json_from()

        await comm1.disconnect()

    @database_sync_to_async
    def _get_message_count(self):
        """Return total Message count (database_sync_to_async wrapper).

        Returns:
            int: Number of Message rows.
        """
        return Message.objects.count()

    @database_sync_to_async
    def _get_message(self, message_id):
        """Retrieve a Message by ID (database_sync_to_async wrapper).

        Args:
            message_id: The primary key of the message.

        Returns:
            Message instance or None.
        """
        try:
            return Message.objects.select_related('user', 'room').get(id=message_id)
        except Message.DoesNotExist:
            return None
