from django.contrib.auth import get_user_model
from django.test import TestCase

from ..exceptions import PermissionsDenied
from ..models import Section, Thread, Post
from ..services import forum_search, toggle_liked, toggle_thread_is_closed


User = get_user_model()


class ForumSearchTestCase(TestCase):
    def setUp(self):
        self.user = User(username='Test', email='t1@e.st', password='1215')
        self.user.save()
        self.other_user = User(username='abu', first_name='abutest', email='t2@e.st', password='1150')
        self.other_user.save()
        self.section = Section(title='test section', description='test', author=self.user)
        self.section.save()
        self.thread = Thread(title='test thread', author=self.user, section=self.section)
        self.thread.save()
        self.thread2 = Thread(title='another thread', author=self.user, section=self.section)
        self.thread2.save()

    def test_search(self):
        result = forum_search('test')
        accounts = result['accounts']
        sections = result['sections']
        threads = result['threads']

        self.assertIn(self.user, accounts)
        self.assertIn(self.other_user, accounts)
        self.assertIn(self.section, sections)
        self.assertIn(self.thread, threads)
        self.assertNotIn(self.thread2, threads)


class ForumToggleLikedTestCase(TestCase):
    def setUp(self):
        self.user = User(username='Test', email='t1@e.st', password='1215')
        self.user.save()
        self.other_user = User(username='abu', first_name='abutest', email='t2@e.st', password='1150')
        self.other_user.save()
        self.section = Section(title='test section', description='test', author=self.user)
        self.section.save()
        self.thread = Thread(title='test thread', author=self.user, section=self.section)
        self.thread.save()

    def test_toggle(self):
        toggle_liked('Section', self.section.pk, self.user)
        self.assertEqual(self.section.likers.count(), 1)

        toggle_liked('Section', self.section.pk, self.other_user)
        self.assertEqual(self.section.likers.count(), 2)

        toggle_liked('Section', self.section.pk, self.other_user)
        self.assertEqual(self.section.likers.count(), 1)

        toggle_liked('Thread', self.thread.pk, self.user)
        self.assertEqual(self.thread.likers.count(), 1)

class ForumToggleThreadIsClosedTestCase(TestCase):
    def setUp(self):
        self.user = User(username='Test', email='t1@e.st', password='1215')
        self.user.save()
        self.other_user = User(username='abu', first_name='abutest', email='t2@e.st', password='1150')
        self.other_user.save()
        self.section = Section(title='test section', description='test', author=self.user)
        self.section.save()
        self.thread = Thread(title='test thread', author=self.user, section=self.section)
        self.thread.save()

    def test_toggle(self):
        self.assertEqual(self.thread.is_closed, False)
        toggle_thread_is_closed(self.thread.pk, self.user)
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.is_closed, True)

        toggle_thread_is_closed(self.thread.pk, self.user)
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.is_closed, False)

    def test_toggle_other_user(self):
        with self.assertRaises(PermissionsDenied):
            toggle_thread_is_closed(self.thread.pk, self.other_user)
