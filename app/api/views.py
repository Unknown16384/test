from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from users.models import UserProfile, Desks
from .serializers import UserListSerializer, UserDetailSerializer, UserDeskSerializer, AdminListSerializer, AdminDetailSerializer

class UserList(generics.ListAPIView):
    queryset = UserProfile.objects.all().prefetch_related('skills', 'skills__skill').select_related('desk')
    serializer_class = UserListSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['skills__skill', 'skills__level']

class UserDetail(generics.RetrieveAPIView):
    queryset = UserProfile.objects.prefetch_related('skills', 'skills__skill').select_related('desk')
    serializer_class = UserDetailSerializer
    lookup_field = 'id'

class UserDesk(generics.RetrieveUpdateAPIView):
    queryset = Desks.objects.select_related('user')
    serializer_class = UserDeskSerializer
    lookup_field = 'user__id'
    lookup_url_kwarg = 'userid'
    permission_classes = [IsAuthenticated]

class AdminList(generics.ListCreateAPIView):
    queryset = User.objects.all().select_related('profile', 'profile__desk').prefetch_related('profile__skills', 'profile__skills__skill')
    serializer_class = AdminListSerializer
    permission_classes = [IsAdminUser]

class AdminDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.prefetch_related('skills', 'skills__skill').select_related('desk', 'user')
    serializer_class = AdminDetailSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUser]
