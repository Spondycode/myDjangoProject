from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Profile, Ride, Poll, PollChoice, Vote
from .serializers import (
    ProfileSerializer, RideListSerializer, RideDetailSerializer,
    PollListSerializer, PollDetailSerializer, VoteSerializer
)


class ProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for user profiles."""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Profile.objects.all()
        # Filter by username if provided
        username = self.request.query_params.get('username', None)
        if username:
            queryset = queryset.filter(user__username=username)
        return queryset
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """Get or update the current user's profile."""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        profile, created = Profile.objects.get_or_create(user=request.user)
        
        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RideViewSet(viewsets.ModelViewSet):
    """ViewSet for rides."""
    queryset = Ride.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return RideListSerializer
        return RideDetailSerializer
    
    def get_queryset(self):
        queryset = Ride.objects.all()
        # Filter upcoming rides
        upcoming = self.request.query_params.get('upcoming', None)
        if upcoming == 'true':
            queryset = queryset.filter(date_time__gt=timezone.now())
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get the next upcoming ride."""
        # First try to get future incomplete rides
        ride = Ride.objects.filter(
            date_time__gt=timezone.now(),
            completed=False
        ).order_by('date_time').first()
        
        # If no future incomplete rides, get the most recent incomplete ride
        if not ride:
            ride = Ride.objects.filter(
                completed=False
            ).order_by('-date_time').first()
        
        if ride:
            serializer = RideDetailSerializer(ride, context={'request': request})
            return Response(serializer.data)
        return Response({'message': 'No upcoming rides'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Join a ride as a participant."""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        ride = self.get_object()
        ride.riders.add(request.user)
        return Response({'message': 'Successfully joined the ride'})
    
    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """Leave a ride."""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        ride = self.get_object()
        ride.riders.remove(request.user)
        return Response({'message': 'Successfully left the ride'})


class PollViewSet(viewsets.ModelViewSet):
    """ViewSet for polls."""
    queryset = Poll.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PollListSerializer
        return PollDetailSerializer
    
    def get_queryset(self):
        queryset = Poll.objects.all()
        # Filter active polls
        active = self.request.query_params.get('active', None)
        if active == 'true':
            queryset = queryset.filter(is_active=True)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get the current active poll."""
        poll = Poll.objects.filter(is_active=True).first()
        
        if poll:
            serializer = PollDetailSerializer(poll, context={'request': request})
            return Response(serializer.data)
        return Response({'message': 'No active polls'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def vote(self, request, pk=None):
        """Submit a vote for this poll."""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        poll = self.get_object()
        choice_id = request.data.get('choice_id')
        
        if not choice_id:
            return Response(
                {'error': 'choice_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            choice = PollChoice.objects.get(id=choice_id, poll=poll)
        except PollChoice.DoesNotExist:
            return Response(
                {'error': 'Invalid choice for this poll'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Remove any existing vote for this poll
        Vote.objects.filter(
            user=request.user,
            choice__poll=poll
        ).delete()
        
        # Create new vote
        vote = Vote.objects.create(user=request.user, choice=choice)
        serializer = VoteSerializer(vote, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Template views for frontend

def home(request):
    """Home page view."""
    return render(request, 'club/home.html')


def logout_view(request):
    """Logout view that redirects to home page."""
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('club:home')


def login_view(request):
    """Login view for members."""
    if request.user.is_authenticated:
        return redirect('club:home')
    
    if request.method == 'POST':
        from django.contrib.auth import authenticate, login
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'club:home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'club/login.html')


def register_view(request):
    """Register view for new members."""
    if request.user.is_authenticated:
        return redirect('club:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        
        # Validation
        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return render(request, 'club/register.html')
        
        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'club/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username "{username}" is already taken.')
            return render(request, 'club/register.html')
        
        # Create user
        from django.contrib.auth import login
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create profile
        Profile.objects.create(user=user)
        
        # Log them in
        login(request, user)
        messages.success(request, f'Welcome to Costa Brava Bikers, {username}!')
        return redirect('club:profile_edit')
    
    return render(request, 'club/register.html')


@login_required
def profile_edit(request):
    """Profile edit page."""
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'club/profile_edit.html', {'profile': profile})


def rides_list(request):
    """Completed rides list page."""
    completed_rides = Ride.objects.filter(completed=True).order_by('-date_time')
    return render(request, 'club/rides_list.html', {'completed_rides': completed_rides})


def ride_detail(request, pk):
    """Ride detail page."""
    ride = get_object_or_404(Ride, pk=pk)
    return render(request, 'club/ride_detail.html', {'ride': ride})


def poll_list(request):
    """Poll list and voting page."""
    return render(request, 'club/poll_list.html')


def members_list(request):
    """Members list page."""
    return render(request, 'club/members_list.html')


def upcoming_ride(request):
    """Upcoming ride detail page."""
    from django.utils import timezone
    # First try to get future incomplete rides
    ride = Ride.objects.filter(date_time__gt=timezone.now(), completed=False).order_by('date_time').first()
    # If no future incomplete rides, get the most recent incomplete ride
    if not ride:
        ride = Ride.objects.filter(completed=False).order_by('-date_time').first()
    return render(request, 'club/upcoming_ride.html', {'ride': ride})


@login_required
def ride_join(request, pk):
    """Join a ride."""
    if request.method == 'POST':
        ride = get_object_or_404(Ride, pk=pk)
        ride.riders.add(request.user)
        messages.success(request, f'You have joined "{ride.title}"!')
        return redirect('club:upcoming_ride')
    return redirect('club:upcoming_ride')


@login_required
def ride_leave(request, pk):
    """Leave a ride."""
    if request.method == 'POST':
        ride = get_object_or_404(Ride, pk=pk)
        ride.riders.remove(request.user)
        messages.success(request, f'You have left "{ride.title}".')
        return redirect('club:upcoming_ride')
    return redirect('club:upcoming_ride')


@staff_member_required
def ride_add(request):
    """Add a new ride (admin only)."""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date_time = request.POST.get('date_time')
        start_point = request.POST.get('start_point')
        end_point = request.POST.get('end_point')
        calimoto_url = request.POST.get('calimoto_url', '')
        relive_url = request.POST.get('relive_url', '')
        header_photo = request.FILES.get('header_photo')
        gpx_file = request.FILES.get('gpx_file')
        
        if not all([title, description, date_time, start_point, end_point]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'club/ride_form.html')
        
        ride = Ride.objects.create(
            title=title,
            description=description,
            date_time=date_time,
            start_point=start_point,
            end_point=end_point,
            calimoto_url=calimoto_url,
            relive_url=relive_url,
            header_photo=header_photo,
            gpx_file=gpx_file,
            created_by=request.user
        )
        
        messages.success(request, f'Ride "{title}" has been created successfully!')
        return redirect('club:upcoming_ride')
    
    return render(request, 'club/ride_form.html', {'edit_mode': False})


@staff_member_required
def ride_edit(request, pk):
    """Edit an existing ride (admin only)."""
    ride = get_object_or_404(Ride, pk=pk)
    
    if request.method == 'POST':
        ride.title = request.POST.get('title', ride.title)
        ride.description = request.POST.get('description', ride.description)
        ride.date_time = request.POST.get('date_time', ride.date_time)
        ride.start_point = request.POST.get('start_point', ride.start_point)
        ride.end_point = request.POST.get('end_point', ride.end_point)
        ride.calimoto_url = request.POST.get('calimoto_url', '')
        ride.relive_url = request.POST.get('relive_url', '')
        
        if 'header_photo' in request.FILES:
            ride.header_photo = request.FILES['header_photo']
        
        if 'gpx_file' in request.FILES:
            ride.gpx_file = request.FILES['gpx_file']
        
        ride.save()
        
        messages.success(request, f'Ride "{ride.title}" has been updated successfully!')
        return redirect('club:upcoming_ride')
    
    return render(request, 'club/ride_form.html', {'ride': ride, 'edit_mode': True})


@staff_member_required
def ride_mark_complete(request, pk):
    """Mark a ride as complete (admin only)."""
    if request.method == 'POST':
        ride = get_object_or_404(Ride, pk=pk)
        ride.completed = True
        ride.save()
        messages.success(request, f'Ride "{ride.title}" has been marked as completed!')
        return redirect('club:upcoming_ride')
    return redirect('club:upcoming_ride')


@staff_member_required
def member_add(request):
    """Add a new member (admin only)."""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        
        # Validate
        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return render(request, 'club/member_add.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username "{username}" already exists.')
            return render(request, 'club/member_add.html')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create profile
        Profile.objects.create(user=user)
        
        messages.success(request, f'Rider "{username}" has been added successfully!')
        return redirect('club:members_list')
    
    return render(request, 'club/member_add.html')


@staff_member_required
def member_delete(request, user_id):
    """Delete a member (admin only)."""
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        
        # Prevent deleting yourself
        if user == request.user:
            return JsonResponse({'error': 'You cannot delete yourself.'}, status=400)
        
        username = user.username
        user.delete()
        
        return JsonResponse({'message': f'Rider "{username}" has been deleted successfully.'})
    
    return JsonResponse({'error': 'Invalid request method.'}, status=400)
