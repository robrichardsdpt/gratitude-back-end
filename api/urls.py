from django.urls import path
from .views.gratitude_views import Gratitudes, GratitudeDetail
from .views.comment_views import Comments, CommentDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword

urlpatterns = [
  	# Restful routing
    path('comments/', Comments.as_view(), name='comments'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='comment_detail'),
    path('gratitudes/', Gratitudes.as_view(), name='gratitudes'),
    path('gratitudes/<int:pk>/', GratitudeDetail.as_view(), name='gratitude_detail'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw')
]
