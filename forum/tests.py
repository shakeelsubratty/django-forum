from django.test import TestCase
from django.test import Client

# Create your tests here.

from .models import Post
from .models import Comment
from .forms import PostForm
from .forms import CommentForm

from django.utils import timezone

# MODEL Test Cases

class PostTestCase(TestCase):
    def setUp(self):
        Post.objects.create(title="Post1",text="This is Post1",date=timezone.now(),author="Shakeel")
        Post.objects.create(title="Post2",text="This is Post2",date=timezone.now(),author="Tabia")

    def test_posts_created(self):
        post1 = Post.objects.get(title="Post1")
        post2 = Post.objects.get(title="Post2")
        self.assertEqual(post1.__str__(),"Post1")
        self.assertEqual(post2.__str__(),"Post2")
        
    def test_posts_text(self):
        post1 = Post.objects.get(title="Post1")
        post2 = Post.objects.get(title="Post2")
        self.assertEquals(post1.text,"This is Post1")
        self.assertEquals(post2.text,"This is Post2")
    
    def test_posts_author(self):
        post1 = Post.objects.get(title="Post1")
        post2 = Post.objects.get(title="Post2")
        self.assertEquals(post1.author,"Shakeel")
        self.assertEquals(post2.author,"Tabia")
        
class CommentTestCase(TestCase):
    def setUp(self):
        Post.objects.create(title="Post1",text="This is Post1",date=timezone.now(),author="Shakeel")
        Post.objects.create(title="Post2",text="This is Post2",date=timezone.now(),author="Tabia")
        post1 = Post.objects.get(title="Post1")
        post2 = Post.objects.get(title="Post2")
        Comment.objects.create(post=post1,title="Comment1",text="This is Comment1",date=timezone.now(),author="Shakeel")
        Comment.objects.create(post=post2,title="Comment2",text="This is Comment2",date=timezone.now(),author="Tabia")

    def test_comments_created(self):
        comment1 = Comment.objects.get(title="Comment1")
        comment2 = Comment.objects.get(title="Comment2")
        self.assertEqual(comment1.__str__(),"Comment1")
        self.assertEqual(comment2.__str__(),"Comment2")
        
    def test_comments_text(self):
        comment1 = Comment.objects.get(title="Comment1")
        comment2 = Comment.objects.get(title="Comment2")
        self.assertEquals(comment1.text,"This is Comment1")
        self.assertEquals(comment2.text,"This is Comment2")
    
    def test_comments_author(self):
        comment1 = Comment.objects.get(title="Comment1")
        comment2 = Comment.objects.get(title="Comment2")
        self.assertEquals(comment1.author,"Shakeel")
        self.assertEquals(comment2.author,"Tabia")
    
#FORMS Test Cases

class PostFormTestCase(TestCase):
    def test_valid_post_form_data(self):
        form = PostForm({
            'title':"Post 1",
            'text':"This is post 1"
        })
        self.assertTrue(form.is_valid())
        post = form.save(commit=False)
        post.author = "k1631133@kcl.ac.uk"
        post.date = timezone.now()
        post.save()
        self.assertEqual(post.title,"Post 1")
        self.assertEqual(post.text,"This is post 1")
        self.assertEqual(post.author,"k1631133@kcl.ac.uk")

    def test_invalid_post_form_data(self):
        form = PostForm({
            'title':"Post 1",
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors,{
            'text': ['This field is required.'],
        })
        form = PostForm({
            'text':"This is Post 1",
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors,{
            'title': ['This field is required.'],
        })
        form = PostForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors,{
            'title': ['This field is required.'],
            'text': ['This field is required.'],
        })
        
class CommentFormTestCase(TestCase):
    def setUp(self):
        Post.objects.create(title="Potato",text="This is Post1",date=timezone.now(),author="Shakeel")
    
    def test_valid_comment_form_data(self):
        post = Post.objects.get(title="Potato")
        form = CommentForm({
            'title':"Comment 1",
            'text':"This is comment 1"
        })
        self.assertTrue(form.is_valid())
        comment = form.save(commit=False)
        comment.post = post
        comment.author = "k1631133@kcl.ac.uk"
        comment.date = timezone.now()
        comment.save()
        self.assertEqual(comment.title,"Comment 1")
        self.assertEqual(comment.text,"This is comment 1")
        self.assertEqual(comment.author,"k1631133@kcl.ac.uk")

    def test_invalid_comment_form_data(self):
        post = Post.objects.get(title="Potato")
        form = CommentForm({
            'title':"Comment 1",
            
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors,{
            'text': ['This field is required.'],
        })
        form = CommentForm({
            'text':"This is Post 1",
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors,{
            'title': ['This field is required.'],
        })
        form = CommentForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors,{
            'title': ['This field is required.'],
            'text': ['This field is required.'],
        })
        
        
class ForumViewsTestCase(TestCase):
    
    def setUp(self):
        Post.objects.create(title="Post1",text="This is Post1",date=timezone.now(),author="Shakeel")
        Post.objects.create(title="Post2",text="This is Post2",date=timezone.now(),author="Tabia")

    
    def test_home(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code,200)
        self.assertTemplateUsed('forum/connect.html')
        
    
    def test_post_new_onGet(self):
        resp = self.client.get('/post/new/')
        self.assertEqual(resp.status_code,200)
        self.assertTemplateUsed('forum/post_edit.html')
        
    def test_post_new_onPost(self):
        session = self.client.session
        session['user_email'] = "k1631133@kcl.ac.uk"
        session.save
        resp = self.client.post('/post/new/')
        self.assertEqual(resp.status_code,200)
        self.assertTemplateUsed('forum/post_detail.html')
        
    def test_comment_new_onGet(self):
        post = Post.objects.get(title="Post1")
        resp = self.client.get('/comment/new',{'id': post.id })
        self.assertTemplateUsed('forum/comment_edit.html')

        