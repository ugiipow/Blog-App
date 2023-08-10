from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic

from .forms import CommentForm
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by("-posted_on")
    template_name = "index.html"
    paginate_by = 5


# class PostDetail(generic.DetailView):
#     model = Post
#     template_name = 'post_detail.html'


def post_detail(request, slug):
    template_name = "post_detail.html"
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True).order_by("-posted_on")
    new_comment = None
    # Comment posted
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            
            new_comment = comment_form.save(commit=False)
            
            new_comment.post = post
            
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render( #context tanımla
        request,
        template_name,
        {
            "post": post,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form,
        },
    )
# def home(request):
#     posts = Post.objects.filter(is_deleted = False)
#     context = dict(
#         posts = posts
#     )
    
#     return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post

    context_object_name = 'posts'
    ordering = ['-posted_on']
    #blog_post = Post.objects.filter(is_deleted = False)

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-posted_on')

# <app> /<model>_<viewtype>.html

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = '__all__'
    template_name = 'add_post.html'

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# def about(request):
#     return render(request, 'blog/about.html', {'title': 'About'})

# def delete_post(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)
#     post.is_deleted = True
#     post.save()
#     return redirect(request, 'post_list')

# def post_list(request):
#     posts = Post.objects.filter(is_deleted=False)
#     return render(request, 'post_list.html', {'posts': posts})