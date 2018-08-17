from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from .forms import PostForm
from .models import Post


def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()

        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not Successfully Created")
    # if request.method =="POST":
    #     print(request.POST.get("content"))
    #     print(request.POST.get("title"))
    #
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)

def post_detail(request, id=None):
    #instance = Post.objects.get(id=2)
    instance = get_object_or_404(Post, id=id) #title="Post 3"
    context = {
        "title": instance.title,
        "instance": instance,
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
    queryset = Post.objects.all()
    context = {
        "object_list" : queryset,
        "title": "List"
    }

    return render(request, "index.html", context)

def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, instance = instance)  #instance = instance ; it adds original data to edit form
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


def post_delete(request, id=None):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Successfully Updated", extra_tags="some-tag")
    return redirect("posts:list")
    return HttpResponseRedirect(instance.get_absolute_url())