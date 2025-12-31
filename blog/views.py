from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post, Comment


class PostList(generic.ListView):
    """
    View to display list of all posts.
    """
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = "blog/index.html"
    context_object_name = 'post_list'


def post_detail(request, slug):
    """
    View to display individual post.
    """
    # Get the post by slug, or return 404 if not found
    post = get_object_or_404(Post, slug=slug, status=1)
    
    # Get approved comments for this post
    comments = post.comments.filter(approved=True)
    
    # Prepare context to pass to template
    context = {
        'post': post,
        'comments': comments,
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
    comment = get_object_or_404(Comment, id=comment_id)
    
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
            
            messages.success(request, 'Comment updated successfully.')
            return redirect('post_detail', slug=slug)
        else:
            messages.error(request, 'Comment cannot be empty.')
    
    context = {
        'comment': comment,
        'post': comment.post,
    }
    return render(request, 'blog/comment_edit.html', context)


@login_required
def comment_delete(request, slug, comment_id):
    """
    View to delete a comment.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if user owns the comment
    if comment.author != request.user:
        messages.error(request, 'You can only delete your own comments.')
        return redirect('post_detail', slug=slug)
    
    comment.delete()
    messages.success(request, 'Comment deleted successfully.')
    return redirect('post_detail', slug=slug)