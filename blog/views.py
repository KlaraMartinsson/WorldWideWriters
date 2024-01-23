from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic, View
from django.contrib import messages
from django.utils.text import slugify
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Post
from .forms import PostForm


# Create your views here.
class HomePage(generic.ListView):
    """
    View to display posts
    """
    model = Post
    queryset = Post.objects.filter(status=1)
    template_name = "blog/index.html"


class PostDetail(View):
    """
    Request the data for a single blog post
    """
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        saved= False
        if post.saved_post.filter(id=self.request.user.id).exists():
            saved = True

        return render(
            request,
            "blog/post_detail.html",
            {"post": post,
            "saved": saved,
            },
        )


def user_post(request):
    """
    View to add form where user can post
    """
    post_form = PostForm()
    if request.method == "POST":
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)
            post.save()  
            messages.add_message(
                request, messages.SUCCESS,
        'Post submitted and awaiting approval'
    )      
      
    return render(
        request,
        "blog/user_post.html",
        {
            "post_form": post_form,
        },
    )


def post_edit(request, id):
    if request.method == "GET":
        post = Post.objects.get(pk=id)
        return render(request, "blog/post_edit.html", {"post": post})
    elif request.method == "POST":
        post = Post.objects.update_or_create(
            pk=id,
            defaults={
                "title": request.POST["title"],
                "content": request.POST["content"],
                "excerpt": request.POST["excerpt"],
                "post_image": request.FILES["post_image"],
            },
        )
        messages.add_message(
                request, messages.SUCCESS,
        'Post edited!'
    )
        return redirect("home")

def post_delete(request, id):
    post = Post.objects.get(pk=id)
    post.delete()
    messages.add_message(
                request, messages.SUCCESS,
        'Post deleted!'
    )
    return redirect("home")


def user_profile(request):
  mydata = Post.objects.all()
  template = loader.get_template('blog/user_profile.html')
  context = {
    'mymembers': mydata,
  }
  return HttpResponse(template.render(context, request))


class PostSaved(View):  

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)

        if post.saved_post.filter(id=request.user.id).exists():
            post.saved_post.remove(request.user)
        else:
            post.saved_post.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))