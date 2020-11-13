from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.gratitude_like import Gratitude_like
from ..serializers import Gratitude_likeSerializer, UserSerializer

# Create your views here.
class Gratitude_likes(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = Gratitude_likeSerializer
    def get(self, request):
        """Index request"""
        # Get all the gratitudes:
        # gratitudes = gratitude.objects.all()
        # Filter the gratitudes by owner, so you can only see your owned gratitudes
        gratitude_likes = Gratitude_like.objects.all()
        # Run the data through the serializer
        data = Gratitude_likeSerializer(gratitude_likes, many=True).data
        return Response({ 'gratitude_likes': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['gratitude_like']['owner'] = request.user.id
        # Serialize/create gratitude
        gratitude_like = Gratitude_likeSerializer(data=request.data['gratitude_like'])
        # If the gratitude data is valid according to our serializer...
        if gratitude_like.is_valid():
            # Save the created gratitude & send a response
            gratitude_like.save()
            return Response({ 'gratitude_like': gratitude_like.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(gratitude_like.errors, status=status.HTTP_400_BAD_REQUEST)

class Gratitude_likeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the gratitude to show
        gratitude_like = get_object_or_404(Gratitude, pk=pk)
        # Only want to show owned gratitudes?

        # Run the data through the serializer so it's formatted
        data = Gratitude_likeSerializer(gratitude_like).data
        return Response({ 'gratitude_like': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate gratitude to delete
        gratitude_like = get_object_or_404(Gratitude_like, pk=pk)
        # Check the gratitude's owner agains the user making this request
        if not request.user.id == gratitude_like.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this gratitude_like')
        # Only delete if the user owns the  gratitude
        gratitude_like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Remove owner from request object
        # This "gets" the owner key on the data['gratitude'] dictionary
        # and returns False if it doesn't find it. So, if it's found we
        # remove it.
        if request.data['gratitude_like'].get('owner', False):
            del request.data['gratitude_like']['owner']

        # Locate gratitude
        # get_object_or_404 returns a object representation of our gratitude
        gratitude_like = get_object_or_404(Gratitude_like, pk=pk)
        # Check if user is the same as the request.user.id
        if not request.user.id == gratitude_like.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this gratitude_like')

        # Add owner to data object now that we know this user owns the resource
        request.data['gratitude_like']['owner'] = request.user.id
        # Validate updates with serializer
        data = Gratitude_likeSerializer(gratitude_like, data=request.data['gratitude_like'])
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
