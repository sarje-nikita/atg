# blog/views.py
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Blog
from .forms import BlogForm


@login_required()
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blog:blog_detail', blog_id=blog.id)
    else:
        form = BlogForm()
    return render(request, 'blog/create_blog.html', {'form': form})

@login_required()
def blog_detail(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    return render(request, 'blog/blog_detail.html', {'blog': blog})


# def blog_list(request):
#     blogs = Blog.objects.filter(draft=False)
#     return render(request, 'blog/blog_list.html', {'blogs': blogs})

# blog/views.py

# @login_required
# def doctor_posts(request):
#     # Filter blog posts by the currently logged-in doctor's ID
#     doctor_posts = Blog.objects.filter(author=request.user)
#     return render(request, 'blog/doctor_posts.html', {'doctor_posts': doctor_posts})
@login_required
def delete_blog(request, blog_id):
    # Retrieve the blog post
    blog = get_object_or_404(Blog, id=blog_id)

    # Check if the user is the author of the blog post
    if request.user == blog.author:
        # Delete the blog post
        blog.delete()
        return redirect('account:doctor')
    else:
        # If the user is not the author, you can return a forbidden response or handle it as needed
        return HttpResponseForbidden("You are not allowed to delete this blog post.")
