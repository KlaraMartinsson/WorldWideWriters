from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post


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
