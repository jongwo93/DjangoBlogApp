from urllib.parse import quote_plus

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils import timezone
from django.db.models import Q
from comments.forms import CommentForm
from comments.models import Comment

from .forms import PostForm
from .models import Post
from .utils import get_read_time


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    # if not request.is_authenticated():
    #     raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()

        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    # if request.method =="POST":
    #     print(request.POST.get("content"))
    #     print(request.POST.get("title"))
    #
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)

def post_detail(request, slug=None):
    #instance = Post.objects.get(id=2)
    instance = get_object_or_404(Post, slug=slug) #title="Post 3"
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)


    print(get_read_time(instance.get_html()))
    # dont need these since i added CommentManager in models.py
    # content_type = ContentType.objects.get_for_model(Post)
    # obj_id = instance.id
    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }

    comment_form = CommentForm(request.POST or None, initial=initial_data)
    if comment_form.is_valid():
        c_type = comment_form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = comment_form.cleaned_data.get("object_id")
        content_data = comment_form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists():
                parent_obj = parent_qs.first()
        new_comment, created = Comment.objects.get_or_create(
                                    user = request.user,
                                    content_type = content_type,
                                    object_id = obj_id,
                                    content = content_data,
                                    parent = parent_obj,
                                )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url()) # this will update the form after commenting.


    comments = instance.comments # Comment.objects.filter_by_instance(instance)


    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        "comments": comments,
        "comment_form": comment_form,
    }
    return render(request, "post_detail.html", context)

def post_list(request): # list items
    # if request.user.is_authenticated():
    #     context = {
    #         "title": "My User List"
    #     }
    # else:
    #     context = {
    #         "title": "List"
    #     }
    today = timezone.now().date()
    queryset_list = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()
    paginator = Paginator(queryset_list, 3)  # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list" : queryset,
        "title": "List",
        "page_request_var": page_request_var,
        "today": today,
    }
    return render(request, "post_list.html", context)


def post_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance = instance)  #instance = instance ; it adds original data to edit form
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()

        messages.success(request, "Successfully Updated", extra_tags="some-tag")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    messages.success(request, "Successfully Updated", extra_tags="some-tag")
    return redirect("posts:list")
