from django.urls import path
from .views import UserSignupView, UserLoginView, GetAllUsers, UserSearchView, FriendRequestView, FriendsListView, PendingFriendRequestsView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('users/', GetAllUsers.as_view(), name='all-users'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('friend-request/', FriendRequestView.as_view(), name='friend-request'),
    path('friend-request/<int:pk>/', FriendRequestView.as_view(), name='friend-request-action'),
    path('friends/', FriendsListView.as_view(), name='friends-list'),
    path('pending-requests/', PendingFriendRequestsView.as_view(), name='pending-requests'),
]
