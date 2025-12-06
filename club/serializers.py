from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Ride, RidePhoto, Poll, PollChoice, Vote


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for Profile model."""
    user = UserSerializer(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'username', 'avatar', 
            'bike_photo_1', 'bike_photo_2', 'bike_photo_3',
            'bio', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RideListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing rides."""
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    rider_count = serializers.SerializerMethodField()
    is_upcoming = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Ride
        fields = [
            'id', 'title', 'date_time', 'start_point', 'end_point',
            'header_photo', 'created_by_username', 'rider_count', 
            'is_upcoming', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_rider_count(self, obj):
        return obj.riders.count()


class RidePhotoSerializer(serializers.ModelSerializer):
    """Serializer for ride photos."""
    uploaded_by = UserSerializer(read_only=True)
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)
    
    class Meta:
        model = RidePhoto
        fields = [
            'id', 'photo', 'caption', 'uploaded_by', 
            'uploaded_by_username', 'order', 'created_at'
        ]
        read_only_fields = ['id', 'uploaded_by', 'created_at']


class RideDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for individual ride."""
    created_by = UserSerializer(read_only=True)
    riders = UserSerializer(many=True, read_only=True)
    rider_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        source='riders',
        write_only=True,
        required=False
    )
    photos = RidePhotoSerializer(many=True, read_only=True)
    is_upcoming = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Ride
        fields = [
            'id', 'title', 'description', 'date_time',
            'header_photo', 'calimoto_url', 'relive_url',
            'start_point', 'end_point', 'gpx_file',
            'created_by', 'riders', 'rider_ids', 'photos',
            'is_upcoming', 'completed', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']


class VoterSerializer(serializers.ModelSerializer):
    """Minimal serializer for voters with avatar info."""
    avatar = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar']
    
    def get_avatar(self, obj):
        try:
            if obj.profile.avatar:
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.profile.avatar.url)
                return obj.profile.avatar.url
        except:
            pass
        return None


class PollChoiceSerializer(serializers.ModelSerializer):
    """Serializer for poll choices."""
    vote_count = serializers.IntegerField(read_only=True)
    voters = serializers.SerializerMethodField()
    percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = PollChoice
        fields = ['id', 'text', 'description', 'vote_count', 'voters', 'percentage']
        read_only_fields = ['id']
    
    def get_voters(self, obj):
        """Get list of users who voted for this choice."""
        votes = Vote.objects.filter(choice=obj).select_related('user', 'user__profile')
        return VoterSerializer([
            vote.user for vote in votes
        ], many=True, context=self.context).data
    
    def get_percentage(self, obj):
        """Calculate percentage of total votes."""
        poll = obj.poll
        total = Vote.objects.filter(choice__poll=poll).count()
        if total == 0:
            return 0
        return round((obj.vote_count / total) * 100, 1)


class PollListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing polls."""
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    choice_count = serializers.SerializerMethodField()
    total_votes = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Poll
        fields = [
            'id', 'title', 'is_active', 'created_by_username',
            'choice_count', 'total_votes', 'created_at', 'closes_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_choice_count(self, obj):
        return obj.choices.count()


class PollDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for individual poll with choices."""
    created_by = UserSerializer(read_only=True)
    choices = PollChoiceSerializer(many=True, read_only=True)
    total_votes = serializers.IntegerField(read_only=True)
    user_vote = serializers.SerializerMethodField()
    
    class Meta:
        model = Poll
        fields = [
            'id', 'title', 'description', 'is_active',
            'created_by', 'choices', 'total_votes', 'user_vote',
            'created_at', 'closes_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at']
    
    def get_user_vote(self, obj):
        """Get the current user's vote for this poll if any."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            vote = Vote.objects.filter(
                user=request.user,
                choice__poll=obj
            ).first()
            if vote:
                return vote.choice.id
        return None


class VoteSerializer(serializers.ModelSerializer):
    """Serializer for voting."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Vote
        fields = ['id', 'user', 'choice', 'voted_at']
        read_only_fields = ['id', 'user', 'voted_at']
    
    def validate(self, data):
        """Validate that user hasn't already voted in this poll."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            choice = data.get('choice')
            existing_vote = Vote.objects.filter(
                user=request.user,
                choice__poll=choice.poll
            ).first()
            
            if existing_vote:
                # Allow changing vote by deleting old one
                existing_vote.delete()
        
        return data
    
    def create(self, validated_data):
        """Create vote with current user."""
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)
