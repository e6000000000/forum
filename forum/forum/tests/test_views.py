import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..models import Section, Thread, Post


User = get_user_model()


class SectionsListTestCase(TestCase):
    def test_get(self):
        url = reverse('index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


class SectionDetailTestCase(TestCase):
    def setUp(self):
        self.user = User(username='testu1', email='t1@e.st', password='1215')
        self.user.save()
        self.section = Section(title='test section', description='test', author=self.user)
        self.section.save()

    def test_get(self):
        url = reverse('section_details', args=(self.section.pk, ))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


class ThreadDetailTestCase(TestCase):
    def setUp(self):
        self.user = User(username='testu1', email='t1@e.st', password='1215')
        self.user.save()
        self.section = Section(title='test section', description='test', author=self.user)
        self.section.save()
        self.thread = Thread(title='test', author=self.user, section=self.section)
        self.thread.save()

    def test_get(self):
        url = reverse('thread_details', args=(self.section.pk, self.thread.pk))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


class SectionCreateTestCase(TestCase):
    def setUp(self):
        self.user = User(username='testu1', email='t1@e.st', password='1215')
        self.user.save()

        self.url = reverse('section_create')

    def test_get_no_login(self):
        response = self.client.get(self.url)

        expected_redirect_url = reverse('login') + '?next=' + self.url
        self.assertRedirects(response, expected_redirect_url)

    def test_get(self):
        self.client.force_login(self.user)        
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.client.force_login(self.user)
        data = {
            'title': 'tts',
            'description': 'fewfewfew',
        }
        response = self.client.post(self.url, data)

        sections = Section.objects.all()
        self.assertEqual(sections.count(), 1)

        section = sections.first() 
        self.assertRedirects(response, section.get_absolute_url())
        self.assertEqual(section.author, self.user)
        self.assertEqual(section.title, 'tts')
        self.assertEqual(section.description, 'fewfewfew')

    
class ThreadCreateTestCase(TestCase):
    def setUp(self):
        self.user = User(username='testu1', email='t1@e.st', password='1215')
        self.user.save()
        self.section = Section(title='test section', description='test', author=self.user)
        self.section.save()

        self.url = reverse('thread_create', args=(self.section.pk, ))

    def test_get_no_login(self):
        response = self.client.get(self.url)

        expected_redirect_url = reverse('login') + '?next=' + self.url
        self.assertRedirects(response, expected_redirect_url)

    def test_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.client.force_login(self.user)
        data = {
            'title': 'tst',
            'posts-TOTAL_FORMS': 1,
            'posts-INITIAL_FORMS': 0,
            'posts-MIN_NUM_FORMS': 0,
            'posts-MAX_NUM_FORMS': 1000,
            'posts-0-text': 'how2',
        }
        response = self.client.post(self.url, data)

        threads = Thread.objects.all()
        self.assertEqual(threads.count(), 1)
        thread = threads.first()

        posts = Post.objects.all()
        self.assertEqual(posts.count(), 1)
        post = posts.first()

        self.assertRedirects(response, thread.get_absolute_url())
        self.assertEqual(thread.author, self.user)
        self.assertEqual(post.author, self.user)
        self.assertEqual(thread.title, 'tst')
        self.assertEqual(post.text, 'how2')
        self.assertEqual(post.thread, thread)


class PostReplyTestCase(TestCase):
    def setUp(self):
        self.user = User(username='testu1', email='t1@e.st', password='1215')
        self.user.save()
        self.section = Section(title='test section', description='test', author=self.user)
        self.section.save()
        self.thread = Thread(title='test thread', author=self.user, section=self.section)
        self.thread.save()
        self.post = Post(author=self.user, text='how2', thread=self.thread)
        self.post.save()

        self.url = reverse('postreply_create', args=(self.section.pk, self.thread.pk, self.post.pk))

    def test_get_no_login(self):
        response = self.client.get(self.url)

        expected_redirect_url = reverse('login') + '?next=' + self.url
        self.assertRedirects(response, expected_redirect_url)

    def test_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.client.force_login(self.user)
        data = {
            'text': 'rtfm',
        }
        response = self.client.post(self.url, data)

        posts = Post.objects.all()
        self.assertEqual(posts.count(), 2)
        new_post = posts.exclude(text='how2').first()

        self.assertRedirects(response, new_post.get_absolute_url())
        self.assertEqual(new_post.text, 'rtfm')
        self.assertEqual(new_post.author, self.user)
        self.assertEqual(new_post.thread, self.thread)


class ThreadIsClosedTestCase(TestCase):
    def setUp(self):
        self.user = User(username='testu1', email='t1@e.st', password='1215')
        self.user.save()
        self.user_other = User(username='testu2', email='t2@e.st', password='1150')
        self.user_other.save()
        self.section = Section(title='test section', description='test', author=self.user)
        self.section.save()
        self.thread = Thread(title='test thread', author=self.user, section=self.section)
        self.thread.save()

        self.url = reverse('thread_update', args=(self.section.pk, self.thread.pk))

    def test_get_no_login(self):
        response = self.client.get(self.url)

        expected_redirect_url = reverse('login') + '?next=' + self.url
        self.assertRedirects(response, expected_redirect_url)

    def test_get_not_author(self):
        self.client.force_login(self.user_other)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)
    
    def test_get_not_author(self):
        thread_is_closed_before_request = self.thread.is_closed

        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.thread.refresh_from_db()

        self.assertRedirects(response, self.thread.get_absolute_url())
        self.assertNotEqual(self.thread.is_closed, thread_is_closed_before_request)


class SearchResultsTestCase(TestCase):
    def test_get(self):
        url = reverse('search') + '?text=test'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


class LikeToggelTestCase(TestCase):
    def setUp(self):
        self.user = User(username='testu1', email='t1@e.st', password='1215')
        self.user.save()
        self.section = Section(title='test section', description='test', author=self.user)
        self.section.save()
        self.thread = Thread(title='test thread', author=self.user, section=self.section)
        self.thread.save()

        self.url = reverse('toggle_like')
    
    def test_post_no_login(self):
        response = self.client.post(self.url)

        expected_redirect_url = reverse('login') + '?next=' + self.url
        self.assertRedirects(response, expected_redirect_url)

    def test_post_section(self):
        likes_count = self.section.likers.count()

        self.client.force_login(self.user)
        data = {
            'model_type': 'Section',
            'pk': self.section.pk,
        }
        response = self.client.post(self.url, json.dumps(data), content_type="application/json")
        
        self.section.refresh_from_db()

        self.assertNotEqual(likes_count, self.section.likers.count())

    def test_post_thread(self):
        likes_count = self.thread.likers.count()

        self.client.force_login(self.user)
        data = {
            'model_type': 'Thread',
            'pk': self.thread.pk,
        }
        response = self.client.post(self.url, json.dumps(data), content_type="application/json")
        
        self.thread.refresh_from_db()

        self.assertNotEqual(likes_count, self.thread.likers.count())







