from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils.text import slugify
from .models import Post
from .forms import PostForm


# Create your views here.
class HomePage(generic.ListView):
    queryset = Post.objects.all()
    template_name = "blog/index.html"


def post_detail(request, slug):
    queryset = Post.objects.all()
    post = get_object_or_404(queryset, slug=slug)

    return render(
        request,
        "blog/post_detail.html",
        {"post": post},
    )


def user_post(request):
    if request.method == "POST":
        post_form = PostForm(data=request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)
            post.save()
            
    post_form = PostForm()
            
    return render(
        request,
        "blog/user_post.html",
        {
            "post_form": post_form,
        },
    )