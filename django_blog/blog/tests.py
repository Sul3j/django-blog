from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db import IntegrityError
from datetime import timedelta
import json

from .models import Post, Comment, Like, Newsletter
from .forms import PostForm, CommentForm, NewsletterForm


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.content, 'Test content')
        self.assertEqual(self.post.author, self.user)
        self.assertIsNotNone(self.post.created_date)
        self.assertIsNone(self.post.published_date)

    def test_post_str_method(self):
        self.assertEqual(str(self.post), 'Test Post')

    def test_post_publish_method(self):
        self.assertIsNone(self.post.published_date)
        self.post.publish()
        self.assertIsNotNone(self.post.published_date)
        self.assertAlmostEqual(
            self.post.published_date,
            timezone.now(),
            delta=timedelta(seconds=1)
        )

    def test_post_author_relationship(self):
        self.assertEqual(self.post.author.username, 'testuser')
        self.assertIn(self.post, self.user.post_set.all())


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            text='Test comment'
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.text, 'Test comment')
        self.assertIsNotNone(self.comment.created_date)
        self.assertFalse(self.comment.approved_comment)

    def test_comment_str_method(self):
        self.assertEqual(str(self.comment), 'Test comment')

    def test_comment_approve_method(self):
        self.assertFalse(self.comment.approved_comment)
        self.comment.approve()
        self.assertTrue(self.comment.approved_comment)

    def test_comment_post_relationship(self):
        self.assertIn(self.comment, self.post.comments.all())

    def test_comment_cascade_delete_with_post(self):
        comment_id = self.comment.id
        self.post.delete()
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(id=comment_id)


class LikeModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass123')
        self.user2 = User.objects.create_user(username='user2', password='testpass123')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user1
        )

    def test_like_creation(self):
        like = Like.objects.create(post=self.post, user=self.user1)
        self.assertEqual(like.post, self.post)
        self.assertEqual(like.user, self.user1)
        self.assertIsNotNone(like.created_date)

    def test_like_unique_constraint(self):
        Like.objects.create(post=self.post, user=self.user1)
        with self.assertRaises(IntegrityError):
            Like.objects.create(post=self.post, user=self.user1)

    def test_multiple_users_can_like_same_post(self):
        like1 = Like.objects.create(post=self.post, user=self.user1)
        like2 = Like.objects.create(post=self.post, user=self.user2)
        self.assertEqual(self.post.likes.count(), 2)
        self.assertIn(like1, self.post.likes.all())
        self.assertIn(like2, self.post.likes.all())

    def test_like_cascade_delete_with_post(self):
        like = Like.objects.create(post=self.post, user=self.user1)
        like_id = like.id
        self.post.delete()
        with self.assertRaises(Like.DoesNotExist):
            Like.objects.get(id=like_id)


class NewsletterModelTest(TestCase):
    def test_newsletter_creation(self):
        newsletter = Newsletter.objects.create(email='test@example.com')
        self.assertEqual(newsletter.email, 'test@example.com')
        self.assertIsNotNone(newsletter.subscribed_date)
        self.assertTrue(newsletter.is_active)

    def test_newsletter_str_method(self):
        newsletter = Newsletter.objects.create(email='test@example.com')
        self.assertEqual(str(newsletter), 'test@example.com')

    def test_newsletter_unique_email(self):
        Newsletter.objects.create(email='test@example.com')
        with self.assertRaises(IntegrityError):
            Newsletter.objects.create(email='test@example.com')

    def test_newsletter_is_active_default(self):
        newsletter = Newsletter.objects.create(email='test@example.com')
        self.assertTrue(newsletter.is_active)


class PostFormTest(TestCase):
    def test_post_form_valid_data(self):
        form = PostForm(data={
            'title': 'Test Title',
            'content': 'Test content'
        })
        self.assertTrue(form.is_valid())

    def test_post_form_missing_title(self):
        form = PostForm(data={
            'content': 'Test content'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_post_form_missing_content(self):
        form = PostForm(data={
            'title': 'Test Title'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

    def test_post_form_empty_data(self):
        form = PostForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_post_form_fields(self):
        form = PostForm()
        self.assertEqual(list(form.fields.keys()), ['title', 'content'])


class CommentFormTest(TestCase):
    def test_comment_form_valid_data(self):
        form = CommentForm(data={'text': 'Test comment'})
        self.assertTrue(form.is_valid())

    def test_comment_form_missing_text(self):
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)

    def test_comment_form_empty_text(self):
        form = CommentForm(data={'text': ''})
        self.assertFalse(form.is_valid())

    def test_comment_form_fields(self):
        form = CommentForm()
        self.assertEqual(list(form.fields.keys()), ['text'])


class NewsletterFormTest(TestCase):
    def test_newsletter_form_valid_email(self):
        form = NewsletterForm(data={'email': 'test@example.com'})
        self.assertTrue(form.is_valid())

    def test_newsletter_form_invalid_email(self):
        form = NewsletterForm(data={'email': 'invalid-email'})
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_newsletter_form_missing_email(self):
        form = NewsletterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_newsletter_form_fields(self):
        form = NewsletterForm()
        self.assertEqual(list(form.fields.keys()), ['email'])


class PostListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')

        self.published_post = Post.objects.create(
            title='Published Post',
            content='Published content',
            author=self.user,
            published_date=timezone.now() - timedelta(days=1)
        )

        self.unpublished_post = Post.objects.create(
            title='Unpublished Post',
            content='Unpublished content',
            author=self.user
        )

        self.future_post = Post.objects.create(
            title='Future Post',
            content='Future content',
            author=self.user,
            published_date=timezone.now() + timedelta(days=1)
        )

    def test_post_list_view_status_code(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)

    def test_post_list_view_template(self):
        response = self.client.get(reverse('post_list'))
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_post_list_shows_only_published_posts(self):
        response = self.client.get(reverse('post_list'))
        posts = response.context['posts']
        self.assertIn(self.published_post, posts)
        self.assertNotIn(self.unpublished_post, posts)
        self.assertNotIn(self.future_post, posts)

    def test_post_list_ordering(self):
        post2 = Post.objects.create(
            title='Newer Post',
            content='Newer content',
            author=self.user,
            published_date=timezone.now()
        )
        response = self.client.get(reverse('post_list'))
        posts = response.context['posts']
        self.assertEqual(posts[0], post2)
        self.assertEqual(posts[1], self.published_post)


class PostDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user,
            published_date=timezone.now()
        )

    def test_post_detail_view_status_code(self):
        response = self.client.get(reverse('post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_view_template(self):
        response = self.client.get(reverse('post_detail', args=[self.post.pk]))
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_post_detail_view_invalid_post(self):
        response = self.client.get(reverse('post_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_post_detail_view_contains_post_content(self):
        response = self.client.get(reverse('post_detail', args=[self.post.pk]))
        self.assertContains(response, 'Test Post')
        self.assertContains(response, 'Test content')

    def test_post_detail_add_comment_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('post_detail', args=[self.post.pk]),
            {'text': 'Test comment'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.text, 'Test comment')
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.post, self.post)

    def test_post_detail_comment_form_in_context(self):
        response = self.client.get(reverse('post_detail', args=[self.post.pk]))
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], CommentForm)


class PostNewViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_post_new_view_login_required(self):
        response = self.client.get(reverse('post_new'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_post_new_view_authenticated_get(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('post_new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_edit.html')
        self.assertIsInstance(response.context['form'], PostForm)

    def test_post_new_view_create_post(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('post_new'),
            {'title': 'New Post', 'content': 'New content'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.title, 'New Post')
        self.assertEqual(post.content, 'New content')
        self.assertEqual(post.author, self.user)
        self.assertIsNotNone(post.published_date)

    def test_post_new_view_invalid_form(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('post_new'), {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), 0)


class PostEditViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.post = Post.objects.create(
            title='Original Title',
            content='Original content',
            author=self.user
        )

    def test_post_edit_view_login_required(self):
        response = self.client.get(reverse('post_edit', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_post_edit_view_authenticated_get(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('post_edit', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_edit.html')
        self.assertIsInstance(response.context['form'], PostForm)

    def test_post_edit_view_update_post(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('post_edit', args=[self.post.pk]),
            {'title': 'Updated Title', 'content': 'Updated content'}
        )
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')
        self.assertEqual(self.post.content, 'Updated content')

    def test_post_edit_view_invalid_post(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('post_edit', args=[9999]))
        self.assertEqual(response.status_code, 404)


class LikePostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user,
            published_date=timezone.now()
        )

    def test_like_post_view_login_required(self):
        response = self.client.get(reverse('like_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)

    def test_like_post_view_create_like(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('like_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['liked'])
        self.assertEqual(data['likes_count'], 1)
        self.assertEqual(Like.objects.count(), 1)

    def test_like_post_view_remove_like(self):
        self.client.login(username='testuser', password='testpass123')
        Like.objects.create(post=self.post, user=self.user)
        response = self.client.get(reverse('like_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['liked'])
        self.assertEqual(data['likes_count'], 0)
        self.assertEqual(Like.objects.count(), 0)

    def test_like_post_view_toggle_functionality(self):
        self.client.login(username='testuser', password='testpass123')

        response1 = self.client.get(reverse('like_post', args=[self.post.pk]))
        data1 = json.loads(response1.content)
        self.assertTrue(data1['liked'])

        response2 = self.client.get(reverse('like_post', args=[self.post.pk]))
        data2 = json.loads(response2.content)
        self.assertFalse(data2['liked'])

        response3 = self.client.get(reverse('like_post', args=[self.post.pk]))
        data3 = json.loads(response3.content)
        self.assertTrue(data3['liked'])

    def test_like_post_view_invalid_post(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('like_post', args=[9999]))
        self.assertEqual(response.status_code, 404)


class NewsletterSignupViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_newsletter_signup_view_success(self):
        response = self.client.post(
            reverse('newsletter_signup'),
            {'email': 'test@example.com'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('post_list'))
        self.assertEqual(Newsletter.objects.count(), 1)
        newsletter = Newsletter.objects.first()
        self.assertEqual(newsletter.email, 'test@example.com')

    def test_newsletter_signup_duplicate_email(self):
        Newsletter.objects.create(email='test@example.com')
        response = self.client.post(
            reverse('newsletter_signup'),
            {'email': 'test@example.com'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Newsletter.objects.count(), 1)

    def test_newsletter_signup_invalid_email(self):
        response = self.client.post(
            reverse('newsletter_signup'),
            {'email': 'invalid-email'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Newsletter.objects.count(), 0)

    def test_newsletter_signup_get_request(self):
        response = self.client.get(reverse('newsletter_signup'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('post_list'))
