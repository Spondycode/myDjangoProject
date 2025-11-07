from django.shortcuts import render


def index(request):
    """Render the main frontend page."""
    return render(request, 'frontend/index.html')
