
from django.test import TestCase
from django.contrib.auth import get_user_model
from blog.models import Post
from django.utils import timezone


User = get_user_model()

class PostTest(TestCase):

    def setUp(self):
        auth1 = User.objects.create(username="author #1")
        auth2 = User.objects.create(username="author #2")

        Post.objects.create(
            title='Blog Post #1',
            text='Dummy text #1',
            author=auth1,
            published_date=timezone.now(),
        )

        Post.objects.create(
            title='Blog Post #2',
            text='Dummy text #2',
            author=auth2,
            published_date=timezone.now(),
        )


    def test_publish_method_for_post(self):
        post = Post.objects.get(title='Blog Post #1')
        post.publish()
        
        self.assertEqual(post.is_published, True)
