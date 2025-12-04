from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Profile(models.Model):
    """Extended user profile for motorcycle club members."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text="Profile picture"
    )
    bike_photo_1 = models.ImageField(
        upload_to='bikes/',
        blank=True,
        null=True,
        help_text="First bike photo"
    )
    bike_photo_2 = models.ImageField(
        upload_to='bikes/',
        blank=True,
        null=True,
        help_text="Second bike photo"
    )
    bike_photo_3 = models.ImageField(
        upload_to='bikes/',
        blank=True,
        null=True,
        help_text="Third bike photo"
    )
    bio = models.TextField(blank=True, help_text="Short bio or description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    class Meta:
        ordering = ['user__username']


class Ride(models.Model):
    """Motorcycle ride details and information."""
    title = models.CharField(max_length=200, help_text="Ride title")
    description = models.TextField(help_text="Detailed description of the ride")
    date_time = models.DateTimeField(help_text="When the ride starts")
    header_photo = models.ImageField(
        upload_to='ride_headers/',
        blank=True,
        null=True,
        help_text="Header image for the ride"
    )
    calimoto_url = models.URLField(
        blank=True,
        max_length=500,
        help_text="Calimoto route URL"
    )
    relive_url = models.URLField(
        blank=True,
        max_length=500,
        help_text="Relive video URL"
    )
    start_point = models.CharField(
        max_length=300,
        help_text="Starting location"
    )
    end_point = models.CharField(
        max_length=300,
        help_text="Ending location"
    )
    gpx_file = models.FileField(
        upload_to='gpx_files/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['gpx'])],
        help_text="GPX route file"
    )
    riders = models.ManyToManyField(
        User,
        related_name='rides',
        blank=True,
        help_text="Members participating in this ride"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_rides',
        help_text="Member who created this ride"
    )
    completed = models.BooleanField(default=False, help_text="Mark as completed after ride is done")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.date_time.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-date_time']

    @property
    def is_upcoming(self):
        """Check if ride is in the future."""
        from django.utils import timezone
        return self.date_time > timezone.now()


class Poll(models.Model):
    """Poll for voting on next ride options."""
    title = models.CharField(max_length=200, help_text="Poll question")
    description = models.TextField(blank=True, help_text="Additional details")
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_polls'
    )
    is_active = models.BooleanField(default=True, help_text="Is this poll currently active")
    created_at = models.DateTimeField(auto_now_add=True)
    closes_at = models.DateTimeField(null=True, blank=True, help_text="When voting closes")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

    @property
    def total_votes(self):
        """Get total number of votes across all choices."""
        return Vote.objects.filter(choice__poll=self).count()


class PollChoice(models.Model):
    """Individual choice option in a poll."""
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200, help_text="Choice option text")
    description = models.TextField(blank=True, help_text="Optional details about this choice")

    def __str__(self):
        return f"{self.poll.title} - {self.text}"

    class Meta:
        ordering = ['id']

    @property
    def vote_count(self):
        """Count votes for this choice."""
        return self.votes.count()


class Vote(models.Model):
    """Individual vote by a user on a poll choice."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    choice = models.ForeignKey(PollChoice, on_delete=models.CASCADE, related_name='votes')
    voted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} voted for {self.choice.text}"

    class Meta:
        # Ensure one vote per user per poll
        unique_together = ['user', 'choice']
        ordering = ['-voted_at']
