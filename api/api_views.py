from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *


@api_view(['GET', 'POST'])
def venue_list(request):
    if request.method == 'GET':
        venues = Venue.objects.all()
        serializer = VenueSerializer(venues, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = VenueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def venue_detail(request, code):
    try:
        venue = Venue.objects.get(pk=code)
    except Venue.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VenueSerializer(venue)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = VenueSerializer(venue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        venue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def hku_member_list(request):
    if request.method == 'GET':
        hku_member = HkuMember.objects.all()
        serializer = HkuMemberSerializer(hku_member, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = HkuMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def hku_member_detail(request, hku_id):
    try:
        hku_member = HkuMember.objects.get(pk=hku_id)
    except HkuMember.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = HkuMemberSerializer(hku_member)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = HkuMemberSerializer(hku_member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        hku_member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def visit_list(request):
    if request.method == 'GET':
        visit = Visit.objects.all()
        serializer = VisitSerializer(visit, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = VisitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def visit_detail(request, visit_id):
    try:
        visit = Visit.objects.get(pk=visit_id)
    except Visit.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VisitSerializer(visit)
        return Response(serializer.data)
