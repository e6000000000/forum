from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


class ProfileDetailTestCase(TestCase):
    def setUp(self):
        self.user1 = User(username='testu', email='t@e.st', password='1215')
        self.user1.save()

    def test_get(self):
        url = reverse('profile', args=(self.user1.pk, ))
        response = self.client.get(url)
        
        self.assertEqual(200, response.status_code)


class ProfileUpdateTestCase(TestCase):
    def setUp(self):
        self.user1 = User(username='testu1', email='t1@e.st', password='1215')
        self.user1.save()

    def test_get_with_no_login(self):
        url = reverse('profile_edit')
        response = self.client.get(url)
        expected_redirect_url = reverse('login') + '?next=' + url

        self.assertRedirects(response, expected_redirect_url) 

    def test_get(self):
        self.client.force_login(self.user1)
        url = reverse('profile_edit')
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)


    def test_post(self):
        self.client.force_login(self.user1)
        url = reverse('profile_edit')
        data = {
            'username': 'ttu',
            'first_name': 'ttf',
            'last_name': 'ttl',
            'bio': 'test bio',
        }
        response = self.client.post(url, data)

        self.assertEqual(302, response.status_code)

        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, 'ttu')
