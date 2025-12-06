# Completed Rides Editing Feature

## Overview
This feature allows members to add photos to completed rides, with different permission levels for admins and regular users.

## Features Implemented

### 1. Photo Gallery System
- **New Model**: `RidePhoto` - stores photos for completed rides
  - Foreign key to Ride
  - Image field for the photo
  - Optional caption
  - Uploaded by (tracks who added the photo)
  - Order field for sorting photos
  - Created timestamp

### 2. Permission-Based Editing

#### Non-Admin Users (Regular Members)
- Can add photos to completed rides
- Can add captions to their photos
- Can delete only their own photos
- View: accessible via "Add Photos" button on completed ride detail pages

#### Admin Users (Staff)
- All non-admin capabilities PLUS:
- Can edit all ride details (title, description, date, locations)
- Can add/update GPX files
- Can add/update Calimoto and Relive links
- Can update the header photo
- Can delete any photo (not just their own)

### 3. User Interface

#### Ride Detail Page (`ride_detail.html`)
- Displays photo gallery for completed rides (if photos exist)
- Shows photo captions and uploader info
- "Add Photos" button for regular users (visible when logged in)
- "Edit Ride & Add Photos" button for admin users

#### Edit Completed Ride Page (`ride_edit_completed.html`)
- Two-column layout:
  - **Left Column**: 
    - Admin-only: Full ride editing form
    - All users: Photo upload form with caption
  - **Right Column**: Photo gallery with delete options
- Responsive design using Tailwind CSS
- Clear permission-based visibility

### 4. URL Routes
- `/rides/<id>/edit-completed/` - Edit completed rides and add photos
- Redirects non-completed rides to regular edit page

### 5. API Integration
- `RidePhotoSerializer` - serializes photo data for API
- `RideDetailSerializer` updated to include photos array
- Photos include uploader info and timestamps

## Usage

### For Members
1. Navigate to a completed ride detail page
2. Click "Add Photos" button
3. Select a photo and optionally add a caption
4. Upload - photo appears in the gallery immediately
5. Can delete own photos using the delete button

### For Admins
1. Navigate to a completed ride detail page
2. Click "Edit Ride & Add Photos" button
3. Use the full form to edit ride details, add GPX files, update links
4. Also upload photos like regular members
5. Can delete any photo in the gallery

## Database Migration
- Migration file: `club/migrations/0003_ridephoto.py`
- Creates the `RidePhoto` table with all necessary fields

## Admin Interface
- `RidePhoto` registered in Django admin
- Sortable by order field
- Filterable by ride and date
- Searchable by ride title, caption, and uploader username

## Files Modified/Created

### Created
- `club/models.py` - Added `RidePhoto` model
- `club/templates/club/ride_edit_completed.html` - Edit page template
- `club/migrations/0003_ridephoto.py` - Database migration
- `COMPLETED_RIDES_FEATURE.md` - This documentation

### Modified
- `club/views.py` - Added `ride_edit_completed` view
- `club/urls.py` - Added URL route for edit completed rides
- `club/admin.py` - Registered `RidePhoto` model
- `club/serializers.py` - Added `RidePhotoSerializer` and updated `RideDetailSerializer`
- `club/templates/club/ride_detail.html` - Added photo gallery and edit button

## Security Considerations
- Login required for all editing operations
- Non-admin users can only delete their own photos
- Admin-only fields are properly protected with `user.is_staff` checks
- CSRF protection on all forms
- Confirmation dialog before photo deletion

## Future Enhancements
- Bulk photo upload
- Photo reordering interface
- Photo comments/reactions
- Photo lightbox/modal view
- Export photos as zip file
