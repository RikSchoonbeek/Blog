import datetime

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect

from urllib.parse import quote_plus

from .forms import PostForm
from .models import Post


# Create your views here.
def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if not request.user.is_authenticated:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    print(form.is_valid())
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "New post is successfully created.", extra_tags="some-tag")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "posts/post_form.html", context)


def post_detail(request, id=None):
    post = get_object_or_404(Post, id=id)
    # Don't show post if it is a draft, or if the publish date is in future.
    if post.draft or post.published > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(post.content)
    context = {
        "post": post,
        "title": post.title,
        "share_string": share_string,
    }
    return render(request, "posts/post_detail.html", context)


def post_list(request):
    post_list_initial = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        post_list_initial = Post.objects.all()
    paginator = Paginator(post_list_initial, 8)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        post_list = paginator.page(paginator.num_pages)
    context = {
        "post_list": post_list,
    }
    return render(request, "posts/post_list.html", context)


def listing(request):
    #contact_list = Contacts.objects.all()
    #paginator = Paginator(contact_list, 25) # Show 25 contacts per page

   # page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'list.html', {'contacts': contacts})


def post_update(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if not request.user.is_authenticated():
        raise Http404
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "The post is successfully updated.")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "post": post,
        "title": post.title,
        "form": form,
    }
    return render(request, "posts/post_form.html", context)


def post_delete(request, id):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if not request.user.is_authenticated():
        raise Http404
    post = get_object_or_404(Post, id=id)
    post.delete()
    messages.success(request, "Post is successfully deleted")
    return redirect("posts:list")


