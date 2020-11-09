from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.comment_like import Comment_like
from ..serializers import Comment_likeSerializer, UserSerializer

# Create your views here.
class Comment_likes(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = Comment_likeSerializer
    def get(self, request):
        """Index request"""
        # Get all the comments:
        # comments = Comment.objects.all()
        # Filter the comments by owner, so you can only see your owned comments
        comment_likes = Comment_like.objects.all()
        # Run the data through the serializer
        data = Comment_likeSerializer(comment_likes, many=True).data
        return Response({ 'comment_likes': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['comment_like']['owner'] = request.user.id
        # Serialize/create comment
        comment_like = Comment_likeSerializer(data=request.data['comment_like'])
        # If the comment data is valid according to our serializer...
        if comment_like.is_valid():
            # Save the created comment & send a response
            comment_like.save()
            return Response({ 'comment_like': comment_like.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(comment_like.errors, status=status.HTTP_400_BAD_REQUEST)

class Comment_likeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the comment to show
        comment_like = get_object_or_404(Comment_like, pk=pk)
        # Only want to show owned comments?
        if not request.user.id == comment_like.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this comment_like')

        # Run the data through the serializer so it's formatted
        data = Comment_likeSerializer(comment_like).data
        return Response({ 'comment_like': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate comment to delete
        comment_like = get_object_or_404(Comment_like, pk=pk)
        # Check the comment's owner agains the user making this request
        if not request.user.id == comment_like.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this comment_like')
        # Only delete if the user owns the  comment
        comment_like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Remove owner from request object
        # This "gets" the owner key on the data['comment'] dictionary
        # and returns False if it doesn't find it. So, if it's found we
        # remove it.
        if request.data['comment_like'].get('owner', False):
            del request.data['comment_like']['owner']

        # Locate comment
        # get_object_or_404 returns a object representation of our comment
        comment_like = get_object_or_404(Comment_like, pk=pk)
        # Check if user is the same as the request.user.id
        if not request.user.id == comment_like.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this comment_like')

        # Add owner to data object now that we know this user owns the resource
        request.data['comment_like']['owner'] = request.user.id
        # Validate updates with serializer
        data = Comment_likeSerializer(comment_like, data=request.data['comment_like'])
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
