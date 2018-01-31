from django.shortcuts import render
from django.http import Http404
from forum.models import Post
from forum.models import Comment

from django.utils import timezone
from django.shortcuts import redirect

# post and comment forms
from .forms import PostForm
from .forms import CommentForm

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from forum.authhelper import get_signin_url
from forum.outlookservice import get_me
from forum.authhelper import get_token_from_code



# this is the origin where the file is opened it calls this methods that returns an html file that shows the root page
def home(request):
  redirect_uri = request.build_absolute_uri(reverse('forum:gettoken'))
  sign_in_url = get_signin_url(redirect_uri)
  return render(request,'forum/connect.html',{
    'sign_in_url' : sign_in_url
  })
# the gettoken function gets the token and we take the information needed for our forum and check if the person is a kings student
def gettoken(request):
  auth_code = request.GET['code']
  redirect_uri = request.build_absolute_uri(reverse('forum:gettoken'))
  token = get_token_from_code(auth_code, redirect_uri)
  access_token = token['access_token']
  user = get_me(access_token)

  # Save the token in the session
  request.session['access_token'] = access_token
  request.session['user_email'] = user['mail']
  request.session['user_name'] = user['displayName']
  context = { 'email': user['mail'] ,
     'name': user['displayName']
  }
  myEmail = user['mail']
  if myEmail is None:
    redirect_uri = request.build_absolute_uri(reverse('forum:gettoken'))
    sign_in_url = get_signin_url(redirect_uri)
    return render(request,'forum/badAnswer.html',{
    'sign_in_url' : sign_in_url
  })
  posts = Post.objects.all()
  return render(request,'forum/index.html',{
       'posts' : posts,
       'email' : user['mail'],
       'user_name' : user['displayName']
   })
# this calls the new post html file and passes the time the post was created along with the author of the post 
def post_new(request):
   if request.method == "POST":
      form = PostForm(request.POST)
      if form.is_valid():
         post = form.save(commit=False)
         post.author = request.session['user_email']
         post.date = timezone.now()
         post.save()
         return redirect('post_detail', id=post.id)
   else:
      form = PostForm()
   return render(request,'forum/post_edit.html', {'form':form})
# this function allows us to create a new comment on a post and passes the author of the comment and when he created it 
def comment_new(request,id):
   if request.method == "POST":
      form = CommentForm(request.POST)
      if form.is_valid():
         comment = form.save(commit=False)
         comment.post = Post.objects.get(id=id)
         comment.author = request.session['user_email']
         comment.date = timezone.now()
         comment.save()
         return  redirect('post_detail',id=id)
   else:
      form = CommentForm()
   post = Post.objects.get(id=id)
   return render(request,'forum/comment_edit.html',{'form':form,'post':post})

# this index function presents the main forum without going back through authentification
def index(request):
   posts = Post.objects.all()
   return render(request,'forum/index.html',{
       'posts' : posts,
        'email' : request.session['user_email'],
       'user_name' : request.session['user_name']
   })
   
# this will show the details of our post by calling the according html file
def post_detail(request,id):
   try:
      post = Post.objects.get(id=id)
      comments = Comment.objects.filter(post__id=id)
   except Post.DoesNotExist:
      raise Http404('This post does not exist')
   return render(request,'forum/post_detail.html',{
      'post' : post,
      'comments' : comments
   })
# the post_delete function allows us to delete a post if we were the creator of this post
def post_delete(request,id):

   post = Post.objects.get(id=id)
   if(post.author == request.session['user_email']):
      post.delete()

   return redirect('index_home')
   
# the comment_delete function allows us to delete a comment if we were the creator of this post
def comment_delete(request,id):
    comment = Comment.objects.get(id=id)
    if(comment.author == request.session['user_email']):
        comment.delete()
        
    return redirect('post_detail',id=comment.post.id)

# the logout function directs to the authentication page
def logout(request):
    return redirect('index')
