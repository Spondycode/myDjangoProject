# Motorcycle Club App

## Overview
A fully-featured Django web application for managing a motorcycle club, including member profiles, ride management, and voting systems.

## Features

### 1. Member Profiles
- Custom profile for each user with avatar and bio
- Upload up to 3 bike photos per member
- View all members and their bikes
- Edit your own profile

### 2. Ride Management
- Create and manage motorcycle rides
- Fields for each ride:
  - Title and description
  - Date and time
  - Start and end locations
  - Header photo
  - Calimoto URL (route planning)
  - Relive URL (video replay)
  - GPX file upload for route data
  - List of participating riders
- Browse all rides (upcoming and past)
- Filter to show only upcoming rides
- Join/leave rides

### 3. Voting System
- Create polls for members to vote on next ride options
- Multiple choice options per poll
- Real-time vote counting and percentages
- Track which poll choices users voted for
- Active poll display on home page

### 4. Home Page
- Displays next upcoming ride
- Quick link to active voting poll
- Quick navigation to all features

## URL Structure

### Frontend Pages
- `/club/` - Home page
- `/club/rides/` - Browse all rides
- `/club/rides/<id>/` - Individual ride details
- `/club/polls/` - Vote on active polls
- `/club/members/` - View all club members
- `/club/profile/edit/` - Edit your profile (requires login)

### API Endpoints
All API endpoints are at `/club/api/`

#### Profiles
- `GET /club/api/profiles/` - List all profiles
- `GET /club/api/profiles/<id>/` - Get profile details
- `GET /club/api/profiles/me/` - Get current user's profile
- `PATCH /club/api/profiles/me/` - Update current user's profile

#### Rides
- `GET /club/api/rides/` - List all rides
- `POST /club/api/rides/` - Create a ride
- `GET /club/api/rides/<id>/` - Get ride details
- `PUT/PATCH /club/api/rides/<id>/` - Update a ride
- `DELETE /club/api/rides/<id>/` - Delete a ride
- `GET /club/api/rides/upcoming/` - Get next upcoming ride
- `POST /club/api/rides/<id>/join/` - Join a ride
- `POST /club/api/rides/<id>/leave/` - Leave a ride

#### Polls
- `GET /club/api/polls/` - List all polls
- `POST /club/api/polls/` - Create a poll
- `GET /club/api/polls/<id>/` - Get poll details
- `PUT/PATCH /club/api/polls/<id>/` - Update a poll
- `DELETE /club/api/polls/<id>/` - Delete a poll
- `GET /club/api/polls/active/` - Get current active poll
- `POST /club/api/polls/<id>/vote/` - Submit a vote

## Database Models

### Profile
- User (OneToOne to Django User)
- Avatar image
- 3 bike photos
- Bio text
- Timestamps

### Ride
- Title, description
- Date/time
- Start/end locations
- Header photo
- Calimoto URL, Relive URL
- GPX file
- Riders (many-to-many with User)
- Created by (ForeignKey to User)
- Timestamps

### Poll
- Title, description
- Is active flag
- Created by (ForeignKey to User)
- Closes at (optional deadline)
- Timestamps

### PollChoice
- Poll (ForeignKey)
- Choice text and description

### Vote
- User (ForeignKey)
- Choice (ForeignKey to PollChoice)
- Timestamp
- Unique constraint: one vote per user per poll

## Admin Interface

All models are registered in the Django admin at `/admin/`:
- Manage profiles with inline editing
- Create/edit rides with fieldsets
- Manage polls with inline choices
- View votes and statistics

## Technology Stack

- **Backend**: Django 5.1, Django REST Framework
- **Frontend**: Tailwind CSS v4, Alpine.js
- **Database**: SQLite (development)
- **Image Processing**: Pillow

## Getting Started

### 1. Run the development server
```bash
.venv/bin/python manage.py runserver
```

### 2. Create a superuser (if not already done)
```bash
.venv/bin/python manage.py createsuperuser
```

### 3. Access the application
- Home: http://localhost:8000/club/
- Admin: http://localhost:8000/admin/
- API: http://localhost:8000/club/api/

### 4. Create sample data
Use the Django admin to create:
1. Profiles for users
2. Some rides (upcoming and past)
3. A poll with choices

## File Uploads

Files are stored in the `media/` directory:
- `media/avatars/` - Profile avatars
- `media/bikes/` - Bike photos
- `media/ride_headers/` - Ride header images
- `media/gpx_files/` - GPX route files

## API Usage Examples

### Get upcoming ride
```bash
curl http://localhost:8000/club/api/rides/upcoming/
```

### Update profile
```bash
curl -X PATCH http://localhost:8000/club/api/profiles/me/ \
  -H "Content-Type: multipart/form-data" \
  -F "bio=Love riding my Harley!" \
  -F "avatar=@/path/to/photo.jpg"
```

### Vote on a poll
```bash
curl -X POST http://localhost:8000/club/api/polls/1/vote/ \
  -H "Content-Type: application/json" \
  -d '{"choice_id": 3}'
```

## Next Steps

1. **Add authentication views** - Implement login/logout/register pages
2. **Email notifications** - Notify members of new rides
3. **Ride comments** - Let members comment on rides
4. **Calendar view** - Display rides in a calendar
5. **GPX parsing** - Display route statistics from GPX files
6. **Social sharing** - Share rides on social media
7. **Mobile app** - Create a mobile companion app
8. **Production database** - Migrate to PostgreSQL for production

## Notes

- The app uses Django's built-in User model
- Profile is created automatically when needed
- All API endpoints support filtering and pagination
- File uploads are validated for correct file types
- Votes are atomic - changing a vote deletes the old one
