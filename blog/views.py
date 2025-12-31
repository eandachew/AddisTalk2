from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Post, Comment


class PostList(generic.ListView):
    """
    View to display list of all published posts.
    """
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = "blog/index.html"
    context_object_name = 'post_list'
    paginate_by = 10  # Optional: add pagination


def post_detail(request, slug):
    """
    View to display individual post with comments.
    """
    # Get the post by slug, or return 404 if not found
    post = get_object_or_404(Post, slug=slug, status=1)
    
    # Get comments for this post (show approved + user's unapproved comments)
    comments = post.comments.filter(approved=True)
    
    # If user is logged in, also show their own unapproved comments
    if request.user.is_authenticated:
        user_unapproved = post.comments.filter(
            author=request.user, 
            approved=False
        )
        comments = comments | user_unapproved
        comments = comments.distinct().order_by('created_on')
    
    # Check if current user has liked the post
    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = post.likes.filter(id=request.user.id).exists()
    
    # Prepare context to pass to template
    context = {
        'post': post,
        'comments': comments,
        'user_has_liked': user_has_liked,
    }
    
    return render(request, 'blog/post_detail.html', context)


@login_required
def add_comment(request, slug):
    """
    View to handle comment submission.
    """
    post = get_object_or_404(Post, slug=slug, status=1)
    
    if request.method == 'POST':
        body = request.POST.get('body', '').strip()
        
        if body:
            # Create comment but don't approve it yet
            comment = Comment.objects.create(
                post=post,
                author=request.user,
                body=body,
                approved=False  # Requires admin approval
            )
            
            messages.success(
                request, 
                'Your comment has been submitted and is awaiting approval.'
            )
        else:
            messages.error(request, 'Comment cannot be empty.')
    
    return redirect('post_detail', slug=post.slug)


@login_required
def comment_edit(request, slug, comment_id):
    """
    View to edit a comment.
    """
    post = get_object_or_404(Post, slug=slug, status=1)
    comment = get_object_or_404(Comment, id=comment_id, post=post)
    
    # Check if user owns the comment
    if comment.author != request.user:
        messages.error(request, 'You can only edit your own comments.')
        return redirect('post_detail', slug=slug)
    
    if request.method == 'POST':
        body = request.POST.get('body', '').strip()
        
        if body:
            comment.body = body
            comment.approved = False  # Needs re-approval after edit
            comment.save()
            
            messages.success(
                request, 
                'Comment updated successfully. It will need admin approval again.'
            )
            return redirect('post_detail', slug=slug)
        else:
            messages.error(request, 'Comment cannot be empty.')
    
    # If GET request, show edit form
    context = {
        'comment': comment,
        'post': post,
    }
    return render(request, 'blog/comment_edit.html', context)


@login_required
def comment_delete(request, slug, comment_id):
    """
    View to delete a comment.
    """
    post = get_object_or_404(Post, slug=slug, status=1)
    comment = get_object_or_404(Comment, id=comment_id, post=post)
    
    # Check if user owns the comment
    if comment.author != request.user:
        messages.error(request, 'You can only delete your own comments.')
        return redirect('post_detail', slug=slug)
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
        return redirect('post_detail', slug=slug)
    
    # If GET request (like from direct URL access), redirect to post
    # This prevents accidental deletion via GET requests
    messages.warning(request, 'Please use the delete button in the comments section.')
    return redirect('post_detail', slug=slug)


@login_required
@require_POST
def post_like(request, slug):
    """
    View to handle post likes (AJAX).
    """
    post = get_object_or_404(Post, slug=slug, status=1)
    
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
        message = "You unliked this post."
    else:
        post.likes.add(request.user)
        liked = True
        message = "You liked this post."
    
    return JsonResponse({
        'liked': liked,
        'like_count': post.likes.count(),
        'message': message
    })


# Optional: View for comment delete confirmation page
@login_required
def comment_confirm_delete(request, slug, comment_id):
    """
    View to show confirmation page for comment deletion.
    This is optional if you want a separate confirmation page instead of modal.
    """
    post = get_object_or_404(Post, slug=slug, status=1)
    comment = get_object_or_404(Comment, id=comment_id, post=post)
    
    # Check if user owns the comment
    if comment.author != request.user:
        messages.error(request, 'You can only delete your own comments.')
        return redirect('post_detail', slug=slug)
    
    context = {
        'post': post,
        'comment': comment,
    }
    return render(request, 'blog/comment_confirm_delete.html', context)