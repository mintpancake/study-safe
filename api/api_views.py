from django.db.models import ExpressionWrapper, F
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from django.db.models import DurationField, F, ExpressionWrapper, Q
import datetime


class VenueList(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        venues = Venue.objects.all()
        serializer = VenueSerializer(venues, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = VenueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VenueDetail(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        try:
            venue = Venue.objects.get(pk=pk)
        except Venue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VenueSerializer(venue)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        try:
            venue = Venue.objects.get(pk=pk)
        except Venue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VenueSerializer(venue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            venue = Venue.objects.get(pk=pk)
        except Venue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        venue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HkuMemberList(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        hku_members = HkuMember.objects.all()
        serializer = HkuMemberSerializer(hku_members, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = HkuMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HkuMemberDetail(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        try:
            hku_member = HkuMember.objects.get(pk=pk)
        except HkuMember.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = HkuMemberSerializer(hku_member)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        try:
            hku_member = HkuMember.objects.get(pk=pk)
        except HkuMember.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = HkuMemberSerializer(hku_member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            hku_member = HkuMember.objects.get(pk=pk)
        except HkuMember.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        hku_member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VisitList(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        visits = Visit.objects.all()
        serializer = VisitSerializer(visits, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = VisitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VisitDetail(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        try:
            visit = Visit.objects.get(pk=pk)
        except Visit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VisitSerializer(visit)
        return Response(serializer.data)


class VisitBy(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, hku_id, date, format=None):
        infectious_date = datetime.datetime.strptime(date, "%d-%m-%Y")
        try:
            visits = Visit.objects.filter(
                hku_member__hku_id=hku_id,
                enter_time__date__gte=datetime.date(infectious_date.year, infectious_date.month, infectious_date.day)
            ) | Visit.objects.filter(
                hku_member__hku_id=hku_id,
                exit_time__date__gte=datetime.date(infectious_date.year, infectious_date.month, infectious_date.day)
            ) | Visit.objects.filter(
                hku_member__hku_id=hku_id,
                exit_time__date__isnull=True
            )
        except Visit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VisitSerializer(visits, many=True)
        return Response(serializer.data)


class CloseContact(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, hku_id, date, format=None):
        infectious_date = datetime.datetime.strptime(date, "%d-%m-%Y") + datetime.timedelta(days=-2)
        try:
            infectious_visits = Visit.objects.filter(
                hku_member__hku_id=hku_id,
                enter_time__date__gte=datetime.date(infectious_date.year, infectious_date.month, infectious_date.day)
            ) | Visit.objects.filter(
                hku_member__hku_id=hku_id,
                exit_time__date__gte=datetime.date(infectious_date.year, infectious_date.month, infectious_date.day)
            ) | Visit.objects.filter(
                hku_member__hku_id=hku_id,
                exit_time__date__isnull=True
            )
        except Visit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        close_contacts = []

        for infectious_visit in infectious_visits:
            venue_i = infectious_visit.venue.code
            enter_time_i = infectious_visit.enter_time
            exit_time_i = infectious_visit.exit_time
            if exit_time_i is None:
                exit_time_i = datetime.datetime.now()

            suspicious_visits = Visit.objects.filter(
                ~Q(hku_member__hku_id=hku_id),
                venue__code=venue_i,
                enter_time__lte=exit_time_i+datetime.timedelta(minutes=-30),
                exit_time__gte=enter_time_i + datetime.timedelta(minutes=30),
            ) & Visit.objects.annotate(diff=ExpressionWrapper(
                F('exit_time') - F('enter_time'), output_field=DurationField()
                )).filter(venue__code=venue_i, diff__gte=datetime.timedelta(minutes=30))

            close_contacts.extend(suspicious_visits)

        close_contact_members = set()

        for close_contact in close_contacts:
            try:
                member = HkuMember.objects.get(hku_id=close_contact.hku_member.hku_id)
                close_contact_members.add(member)
            except HkuMember.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = HkuMemberSerializer(close_contact_members, many=True)
        return Response(serializer.data)
