from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.comment import Comment
from ..serializers import CommentSerializer, UserSerializer

# Create your views here.
class Comments(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = CommentSerializer
    def get(self, request):
        """Index request"""
        # Get all the comments:
        # comments = Comment.objects.all()
        # Filter the comments by owner, so you can only see your owned comments
        comments = Comment.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = CommentSerializer(comments, many=True).data
        return Response({ 'comments': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['comment']['owner'] = request.user.id
        # Serialize/create comment
        comment = CommentSerializer(data=request.data['comment'])
        # If the comment data is valid according to our serializer...
        if comment.is_valid():
            # Save the created comment & send a response
            comment.save()
            return Response({ 'comment': comment.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(comment.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the comment to show
        comment = get_object_or_404(Comment, pk=pk)
        # Only want to show owned comments?
        if not request.user.id == comment.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this comment')

        # Run the data through the serializer so it's formatted
        data = CommentSerializer(comment).data
        return Response({ 'comment': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate comment to delete
        comment = get_object_or_404(Comment, pk=pk)
        # Check the comment's owner agains the user making this request
        if not request.user.id == comment.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this comment')
        # Only delete if the user owns the  comment
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Remove owner from request object
        # This "gets" the owner key on the data['comment'] dictionary
        # and returns False if it doesn't find it. So, if it's found we
        # remove it.
        if request.data['comment'].get('owner', False):
            del request.data['comment']['owner']

        # Locate comment
        # get_object_or_404 returns a object representation of our comment
        comment = get_object_or_404(Comment, pk=pk)
        # Check if user is the same as the request.user.id
        if not request.user.id == comment.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this comment')

        # Add owner to data object now that we know this user owns the resource
        request.data['comment']['owner'] = request.user.id
        # Validate updates with serializer
        data = CommentSerializer(comment, data=request.data['comment'])
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
