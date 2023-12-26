from django.shortcuts import render, get_object_or_404, redirect

from blog.models import Post
from .forms import PostForm, CommentForm

from django.http import Http404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def post_list(request):
    posts = Post.objects.for_user(user=request.user).order_by('-published_date')
    return render(request, 'post_list.html', {'posts' : posts})

# commit 

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    if not post.is_published and not request.user.is_staff:
        raise Http404('Запись в блоге не найдена')
    return render(request, 'post_detail.html', {'post' : post})


def post_add(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                if post.is_published:
                    post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', id=post.id)
        else:
            form = PostForm()

        return render(request, 'post_edit.html', {'form' : form})
    return redirect('post_list')

@login_required
def post_publish(request, id):
    post = get_object_or_404(Post, id=id)
    post.publish()
    return redirect('post_detail', id=id)


@login_required
def post_edit(request, id=None):
    post = get_object_or_404(Post, id=id) if id else None
    if post and request.user != post.author:
        return redirect('post_list')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            if post.is_published:
                post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm(instance=post)
        
    return render(request, 'post_edit.html', {'form' : form})

@login_required
def add_comment(request, id):
    post = get_object_or_404(Post, id=id)
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comm = form.save(commit=False)
            comm.post = post
            comm.author = request.user  # Устанавливаем автора комментария
            comm.save()
            return redirect('post_detail', id=post.id)
    else:
        initial_data = {'author': request.user.username}  # Устанавливаем начальное значение автора
        form = CommentForm(initial=initial_data)
    return render(request, 'add_comment.html', {'form': form, 'post': post})

@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    
    if request.user != post.author:
        messages.error(request, 'У вас нет прав для удаления этого поста.')
        return redirect('post_list')

    if request.method == "POST":
        post.delete()
        messages.success(request, 'Пост успешно удален.')
        return redirect('post_list')
    
    return render(request, 'post_delete.html', {'post': post})



# обработчик 404
'''
def handler404(request, exception, template_name='404.html'):
    response = render(request, template_name)
    response.status_code = 404
    return response
'''