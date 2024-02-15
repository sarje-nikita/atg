from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from blog.models import Blog
from django.http import JsonResponse



# Create your views here.


def index(request):
    return render(request, 'index.html')


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form.is_valid():
            user = form.save()
            msg = 'User created successfully'
            return redirect('account:login_view')
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None and user.is_patient:
                login(request, user)
                return redirect('account:patient')
            elif user is not None and user.is_doctor:
                login(request, user)
                return redirect('account:doctor')
            else:
                msg = 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})


@login_required
def patient(request):
    if request.user.is_patient:
        categorized_posts = {}
        posts = Blog.objects.filter(draft=False)  # Filter posts not marked as draft
        for post in posts:
            if post.category in categorized_posts:
                categorized_posts[post.category].append(post)
            else:
                categorized_posts[post.category] = [post]

        return render(request, 'patient_dashboard.html', {'user': request.user, 'categorized_posts': categorized_posts})
    else:
        return redirect('/')






# @login_required
# def doctor(request):
#     if request.user.is_doctor:
#         return render(request, 'doctor_dashboard.html', {'user': request.user})
#     else:
#         return redirect('/')
#

# views.py


def doctor(request):
    # Retrieve the doctor's blog posts
    categorized_posts = {}
    doctor_posts = Blog.objects.filter(author=request.user)
    for post in doctor_posts:
        if post.category in categorized_posts:
            categorized_posts[post.category].append(post)
        else:
            categorized_posts[post.category] = [post]
    return render(request, 'doctor_dashboard.html', {'doctor_posts': categorized_posts, 'user': request.user})

# @login_required
# def doctor_blog_list(request):
#     # Retrieve blog posts for the current doctor
#     blogs = Blog.objects.filter(author=request.user)
#     return render(request, 'blog/doctor_blog_list.html', {'blogs': blogs})

@login_required
def publish_draft(request, blog_id):
    # Publish a draft blog post
    blog = get_object_or_404(Blog, id=blog_id, author=request.user)
    blog.publish()
    return redirect('account:doctor')


@login_required
def logout_view(request):
    logout(request)
    return redirect('account:index')

@login_required
def home(request):
    if request.user.is_doctor:
        return redirect('account:doctor')
    else:
        return redirect('account:patient')

@login_required
def blog_data(request):
    doctor_posts = Blog.objects.filter(author=request.user)
    total_blogs = doctor_posts.count()
    categories = {}
    for post in doctor_posts:
        if post.category in categories:
            categories[post.category] += 1
        else:
            categories[post.category] = 1
    return JsonResponse({'totalBlogs': total_blogs, 'categories': categories})