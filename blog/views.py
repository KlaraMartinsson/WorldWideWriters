from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic, View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from cloudinary.models import CloudinaryField

from .models import Post, Rating

from .forms import PostForm, RatingForm


class HomePage(generic.ListView):
    """
    View to display homepage
    """
    model = Post
    template_name = "blog/index.html"


class PostList(generic.ListView):
    """
    View to display posts
    """
    model = Post
    queryset = Post.objects.filter(status=1)
    template_name = "blog/post_list.html"


def post_detail(request, slug):
    """
    Request the data for a single blog post
    """
    queryset = Post.objects.all()
    post = get_object_or_404(queryset, slug=slug)
    saved = False

    if post.saved_post.filter(id=request.user.id).exists():
        saved = True

    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(
            user=request.user, post=post).exists()
    else:
        user_rating = False

    if request.method == "POST":
        if 'rating_form' in request.POST:
            rating_form = RatingForm(data=request.POST)
            if rating_form.is_valid() and request.user.is_authenticated:
                rating = rating_form.save(commit=False)
                rating.user = request.user
                rating.post = post
                rating.save()
                messages.success(request, "Post rating submitted.")
                return HttpResponseRedirect(
                    reverse('post_detail', args=[slug]))
            else:
                messages.error(
                    request, "Error rating post. Please try again.")

    rating_form = RatingForm()

    context = {
        "post": post,
        "saved": saved,
        "user_rating": user_rating,
        "rating_form": rating_form,
    }
    return render(request, "blog/post_detail.html", context)


def user_post(request):
    """
    View to add form where user can post
    """
    post_form = PostForm()
    if request.method == "POST":
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid() and request.user.is_authenticated:
            post = post_form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)
            post.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Post submitted and awaiting approval')
        return redirect("user_profile")

    return render(
        request,
        "blog/user_post.html",
        {
            "post_form": post_form,
        },
    )


def post_edit(request, id):
    """
    View for users to edit their posts
    """
    post = Post.objects.get(pk=id)
    if post.author == request.user:
        if request.method == "POST":
            post_form = PostForm(request.POST, request.FILES, instance=post)
            if post_form.is_valid():
                post_form.save()
                messages.add_message(request, messages.SUCCESS, 'Post edited!')
                return redirect("user_profile")
            else:
                messages.add_message(request, messages.ERROR,
                                     'Error editing post.')
                return redirect("user_profile")
        else:
            post_form = PostForm(instance=post)
    else:
        messages.add_message(request, messages.ERROR,
                             'Error, you can only edit your own posts.')
        return redirect("user_profile")
    return render(request, "blog/post_edit.html",
                  {"post": post, "post_form": post_form})


def post_delete(request, id):
    """
    View for users to delete their posts
    """
    post = Post.objects.get(pk=id)
    if post.author == request.user:
        post.delete()
        messages.add_message(request, messages.SUCCESS, 'Post deleted!')
    else:
        messages.add_message(request, messages.ERROR,
                             'Error from deleting the post.')
    return redirect("user_profile")


@login_required
def user_profile(request):
    """
    View to display posts in user profile
    """
    mydata = Post.objects.all()
    template = loader.get_template('blog/user_profile.html')
    context = {
        'mymembers': mydata,
    }
    return HttpResponse(template.render(context, request))


class PostSaved(View):
    """
    View for users to save posts in their profile
    """
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)

        if post.saved_post.filter(id=request.user.id).exists():
            post.saved_post.remove(request.user)
            messages.add_message(
                request, messages.SUCCESS,
                'Post unsaved!')
        else:
            post.saved_post.add(request.user)
            messages.add_message(
                request, messages.SUCCESS,
                'Post saved!')
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class ContinentPosts(generic.ListView):
    """
    View to filter posts by continent
    """
    model = Post
    template_name = 'blog/continent_posts.html'
    """
    Default to 'None' if not provided
    """
    def get_queryset(self):
        continent = self.kwargs.get('continent', 0)
        return Post.objects.filter(continents=continent, status=1)


def custom_404(request, exception):
    """
    View to load 404 page
    """
    return render(request, '404.html', status=404)
