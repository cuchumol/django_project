
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from blog.models import Post
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from blog.serializer import BlogPostListSerializer, BlogPostDetailSerializer


User = get_user_model()

client = Client()

class PostTest(TestCase):

    def setUp(self):
        auth1 = User.objects.create(username="author #1")
        auth2 = User.objects.create(username="author #2")

        Post.objects.create(
            title='Blog Post #1',
            text='Dummy text #1',
            author=auth1,
        )

        Post.objects.create(
            title='Blog Post #2',
            text='Dummy text #2',
            author=auth2,
        )


        Post.objects.create(
            title='Blog Post #3',
            text='Dummy text #3',
            author=auth2,
            is_published=True,
            published_date=timezone.now()
        )

    def test_publish_method_for_post(self):
        post = Post.objects.get(title='Blog Post #1')
        post.publish()
        
        self.assertEqual(post.is_published, True)


    def test_published_post_filtering(self):
        posts = Post.published.all()
        self.assertEqual(posts.count(), 1)


class GetAllPostsTest(TestCase):
    
    def setUp(self):
        auth1 = User.objects.create(username="author #1")

        Post.objects.create(
            title='Blog Post #1',
            text='Dummy text #1',
            author=auth1,
        )

        Post.objects.create(
            title='Blog Post #2',
            text='Dummy text #2',
            author=auth1,
        )


        Post.objects.create(
            title='Blog Post #3',
            text='Dummy text #3',
            author=auth1,
        )

    def test_get_all_posts(self):
        response = client.get(reverse('post-list'))
        posts = Post.objects.all()
        serializer = BlogPostListSerializer(posts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class GetSinglePostTest(TestCase):
    def setUp(self):
        auth1 = User.objects.create(username="author #1")

        self.post = Post.objects.create(
            title='Blog Post #1',
            author=auth1,
        )

    
    def test_get_valid_single_post(self):
        response = client.get(reverse('post-detail', kwargs={'pk' : self.post.pk}))

        post = Post.objects.get(pk=self.post.pk)
        serializer = BlogPostDetailSerializer(post)


        excluded_fields = ['comments_count', 'comments']

        filtered_data = {key: value for key, value in serializer.data.items() if key not in excluded_fields}

        self.assertEqual(filtered_data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_invalid_single_post(self):
        response = client.get(reverse('post-detail', kwargs={'pk' : 99999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        
