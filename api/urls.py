from django.urls import path
from .views.gratitude_views import Gratitudes, GratitudeDetail
from .views.comment_views import Comments, CommentDetail
from .views.gratitude_like_views import Gratitude_likes, Gratitude_likeDetail
from .views.comment_like_views import Comment_likes, Comment_likeDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword

urlpatterns = [
  	# Restful routing
    path('comments/', Comments.as_view(), name='comments'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='comment_detail'),
    path('comment_likes/', Comment_likes.as_view(), name='comment_likes'),
    path('comment_likes/<int:pk>/', Comment_likeDetail.as_view(), name='comment_like_detail'),
    path('gratitudes/', Gratitudes.as_view(), name='gratitudes'),
    path('gratitudes/<int:pk>/', GratitudeDetail.as_view(), name='gratitude_detail'),
    path('gratitude_likes/', Gratitude_likes.as_view(), name='gratitude_likes'),
    path('gratitude_likes/<int:pk>/', Gratitude_likeDetail.as_view(), name='gratitude_like_detail'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw')
]
