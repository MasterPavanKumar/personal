from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
# from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from .models import User,FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
# import ipdb
# User = get_user_model()

class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email').lower()
        pas = request.data.get('password')
        print(f"Email: {email}, Password: {pas}")
        # ipdb.set_trace()
        user = User.objects.filter(email=email, password=pas).first()
        print(user)
        if user:
            print("ENTERED HERE REY")
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return User.objects.filter(Q(email__icontains=query) | Q(name__icontains=query))
    
class GetAllUsers(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class FriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        to_user_id = request.data.get('to_user_id')
        to_user = User.objects.filter(id=to_user_id).first()
        if to_user:
            if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
                return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)
            now = timezone.now()
            one_minute_ago = now - timedelta(minutes=1)
            recent_requests = FriendRequest.objects.filter(from_user=request.user, timestamp__gte=one_minute_ago)
            if recent_requests.count() >= 3:
                return Response({'error': 'Cannot send more than 3 friend requests within a minute'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
            friend_request = FriendRequest(from_user=request.user, to_user=to_user)
            friend_request.save()
            return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        friend_request = FriendRequest.objects.filter(id=pk, to_user=request.user, status='pending').first()
        if friend_request:
            action = request.data.get('action')
            if action == 'accept':
                friend_request.status = 'accepted'
                friend_request.save()
                return Response(FriendRequestSerializer(friend_request).data)
            elif action == 'reject':
                friend_request.status = 'rejected'
                friend_request.save()
                return Response(FriendRequestSerializer(friend_request).data)
        return Response({'error': 'Friend request not found or already acted upon'}, status=status.HTTP_404_NOT_FOUND)

class FriendsListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(sent_requests__to_user=self.request.user, sent_requests__status='accepted')

class PendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status='pending')
