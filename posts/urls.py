from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/', views.index, name="post"),
    path('upload/', views.addPost, name="addPost"),
    path('select-thumbnail/', views.selectThumbnail, name="selectThumbnail"),
    path('<int:id>/add-comment/', views.addComment, name="addComment"),
    path('<int:post_id>/added-comment/<int:comment_id>/', views.addedComment, name="addedComment"),
    path('<int:post_id>/comment-option/<int:comment_id>/', views.commentOption, name="commentOption"),
    path('<int:post_id>/del-comment/<int:comment_id>/', views.deleteComment, name="deleteComment"),
    path('<int:post_id>/new-comments/<int:last_cm_id>/', views.newComment, name="newComment"),
    path('<int:post_id>/comment/<int:comment_id>/add-reply/', views.addReply, name="addReply"),
    path('<int:post_id>/comment/<int:comment_id>/added-reply/<int:reply_id>/', views.addedReply, name="addedReply"),
    path('<int:post_id>/comment/<int:comment_id>/view-replies/', views.viewReply, name="viewReply"),
    path('<int:post_id>/comment/<int:comment_id>/del-reply/<int:reply_id>/', views.deleteReply, name="deleteReply"),
] 
