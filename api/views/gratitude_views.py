from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.gratitude import Gratitude
from ..serializers import GratitudeSerializer, UserSerializer

# Create your views here.
class Gratitudes(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = GratitudeSerializer
    def get(self, request):
        """Index request"""
        # Get all the gratitudes:
        # gratitudes = gratitude.objects.all()
        # Filter the gratitudes by owner, so you can only see your owned gratitudes
        gratitudes = Gratitude.objects.all()
        data = GratitudeSerializer(gratitudes, many=True).data
        sorted_data = sorted(data, key = lambda i : i['id'], reverse=True)
        # Run the data through the serializer
        return Response({ 'gratitudes': sorted_data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['gratitude']['owner'] = request.user.id
        # Serialize/create gratitude
        gratitude = GratitudeSerializer(data=request.data['gratitude'])
        # If the gratitude data is valid according to our serializer...
        if gratitude.is_valid():
            # Save the created gratitude & send a response
            gratitude.save()
            return Response({ 'gratitude': gratitude.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(gratitude.errors, status=status.HTTP_400_BAD_REQUEST)

class GratitudeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the gratitude to show
        gratitude = get_object_or_404(Gratitude, pk=pk)
        # Only want to show owned gratitudes?
        if not request.user.id == gratitude.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this gratitude')

        # Run the data through the serializer so it's formatted
        data = GratitudeSerializer(gratitude).data
        return Response({ 'gratitude': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate gratitude to delete
        gratitude = get_object_or_404(Gratitude, pk=pk)
        # Check the gratitude's owner agains the user making this request
        if not request.user.id == gratitude.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this gratitude')
        # Only delete if the user owns the  gratitude
        gratitude.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Remove owner from request object
        # This "gets" the owner key on the data['gratitude'] dictionary
        # and returns False if it doesn't find it. So, if it's found we
        # remove it.
        if request.data['gratitude'].get('owner', False):
            del request.data['gratitude']['owner']

        # Locate gratitude
        # get_object_or_404 returns a object representation of our gratitude
        gratitude = get_object_or_404(Gratitude, pk=pk)
        # Check if user is the same as the request.user.id
        if not request.user.id == gratitude.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this gratitude')

        # Add owner to data object now that we know this user owns the resource
        request.data['gratitude']['owner'] = request.user.id
        # Validate updates with serializer
        data = GratitudeSerializer(gratitude, data=request.data['gratitude'])
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
