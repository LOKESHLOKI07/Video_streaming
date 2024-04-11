from datetime import datetime

from django.shortcuts import render, redirect
from django.views.generic import ListView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Video
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import VideoForm
from django.contrib.auth import authenticate, login

# Serializer
from rest_framework import serializers

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

@login_required
@api_view(['GET', 'POST'])
def video_list(request):
    if request.method == 'GET':
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
@api_view(['GET', 'PUT', 'DELETE'])
def video_detail(request, pk):
    try:
        # Try to retrieve the video object with the given primary key
        video = Video.objects.get(pk=pk)
    except Video.DoesNotExist:
        # If the video does not exist, return a 404 Not Found response
        return Response(status=status.HTTP_404_NOT_FOUND)

    # If the request method is GET, retrieve and return the video details
    if request.method == 'GET':
        serializer = VideoSerializer(video)
        return Response(serializer.data)

    # If the request method is PUT, update the video details with the provided data
    elif request.method == 'PUT':
        serializer = VideoSerializer(video, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # If the request method is DELETE, delete the video from the database
    elif request.method == 'DELETE':
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@login_required
def video_search(request):
    query = request.GET.get('query')
    videos = Video.objects.all()  # Default queryset

    if query:
        videos = Video.objects.filter(title__icontains=query)

    return render(request, 'videos/video_search.html', {'videos': videos, 'query': query})

@login_required
def video_create(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('video-list')
    else:
        form = VideoForm()
    return render(request, 'videos/video_form.html', {'form': form})

@login_required
def video_update(request, pk):
    try:
        video = Video.objects.get(pk=pk)
    except Video.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            return redirect('video-detail', pk=pk)
    else:
        form = VideoForm(instance=video)
    return render(request, 'videos/video_form.html', {'form': form})

@login_required
def video_delete(request, pk):
    try:
        video = Video.objects.get(pk=pk)
    except Video.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        video.delete()
        return redirect('video-list')
    return render(request, 'videos/video_confirm_delete.html', {'video': video})

@login_required
def user_profile(request):
    user = request.user
    return render(request, 'videos/user_profile.html', {'user': user})

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or perform other actions
    else:
        form = UserRegistrationForm()

    return render(request, 'videos/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome back, {}. You are now logged in.'.format(username))
            return redirect('video-create')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    else:
        return render(request, 'videos/login.html')

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]


import cv2
from django.http import StreamingHttpResponse
from django.views.decorators import gzip

# Define a function to read video frames and stream them
def generate_frames():
    for video in Video.objects.all():
        cap = cv2.VideoCapture(video.video_file.path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        cap.release()

@gzip.gzip_page
def video_stream(request):
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def calculate_oee(availability, performance, quality):
    return availability * performance * quality
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Machine, ProductionLog

@api_view(['GET'])
def oee_data(request):
    # Retrieve data from the database and calculate OEE
    # You'll need to implement this logic based on your specific requirements
    # Example:
    machines = Machine.objects.all()
    oee_data = []
    for machine in machines:
        # Calculate availability, performance, and quality
        availability = calculate_availability(machine)
        performance = calculate_performance(machine)
        quality = calculate_quality(machine)
        oee = calculate_oee(availability, performance, quality)
        oee_data.append({'machine_name': machine.machine_name, 'oee': oee})
    return Response(oee_data)


@api_view(['GET'])
def oee_data_filtered(request):
    # Get parameters from the request
    machine_name = request.GET.get('machine_name')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Convert start_date and end_date to datetime objects if they exist
    start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
    end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None

    # Filter production data based on provided parameters
    queryset = ProductionLog.objects.all()
    if machine_name:
        queryset = queryset.filter(machine__machine_name=machine_name)
    if start_date and end_date:
        # Filter based on start_time between start_date and end_date
        queryset = queryset.filter(start_time__range=(start_date, end_date))

    # Serialize the filtered data
    serializer = ProductionLogSerializer(queryset, many=True)

    # Return the serialized data in the response
    return Response(serializer.data)


def test(request):

    return render(request, 'videos/test.html', )

def video_only(request):
    videos = Video.objects.all()
    return render(request, 'videos/video-list.html', {'videos': videos})




# Import necessary modules
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Machine, ProductionLog
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ProductionLogForm
from django.contrib.auth import authenticate, login
from rest_framework import status

# Serializer for ProductionLog
from rest_framework import serializers

class ProductionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionLog
        fields = '__all__'

@login_required
@api_view(['POST'])
def add_production_entry(request):
    if request.method == 'POST':
        form = ProductionLogForm(request.POST)
        if form.is_valid():
            form.save()
            return Response({'message': 'Production entry added successfully.'}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
def user_profile(request):
    user = request.user
    return render(request, 'videos/user_profile.html', {'user': user})

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class ProductionLogViewSet(viewsets.ModelViewSet):
    queryset = ProductionLog.objects.all()
    serializer_class = ProductionLogSerializer
    permission_classes = [IsAuthenticated]

# Implement functions to calculate availability, performance, and quality
def calculate_availability(machine):

    available_time = 24 * 30 * 3  # Assuming 3 shifts per day and 30 days in a month
    downtime = 0  # Assuming no downtime for simplicity
    availability = (available_time - downtime) / available_time * 100
    return availability


def calculate_performance(machine):
    # Implement logic to calculate performance
    # Performance = (Ideal Cycle Time * Actual Output) / Available Operating Time * 100
    ideal_cycle_time = 5  # Ideal cycle time is 5 minutes
    actual_output = ProductionLog.objects.filter(machine=machine).count()
    available_operating_time = actual_output * ideal_cycle_time

    if available_operating_time == 0:
        return 0  # Avoid division by zero

    performance = (ideal_cycle_time * actual_output) / available_operating_time * 100
    return performance


def calculate_quality(machine):
    # Assuming shorter duration indicates better quality
    # You can adjust this logic based on your specific requirements
    good_duration_threshold = 5  # Threshold for considering duration as good
    good_products = ProductionLog.objects.filter(machine=machine, duration__lte=good_duration_threshold).count()

    total_products = ProductionLog.objects.filter(machine=machine).count()
    if total_products == 0:
        return 0  # Avoid division by zero
    quality = (good_products / total_products) * 100
    return quality



def calculate_oee(availability, performance, quality):
    # Implement logic to calculate Overall Equipment Effectiveness (OEE)
    # OEE = Availability * Performance * Quality
    return availability * performance * quality / 10000  # Dividing by 10000 to get percentage

# Implement API views to compute and provide OEE data
@api_view(['GET'])
def oee_data(request):
    machines = Machine.objects.all()
    oee_data = []
    for machine in machines:
        availability = calculate_availability(machine)
        performance = calculate_performance(machine)
        quality = calculate_quality(machine)
        oee = calculate_oee(availability, performance, quality)
        oee_data.append({'machine_name': machine.machine_name, 'oee': oee})
    return Response(oee_data)

# Add functionality to add production entries to the database based on the provided information
@login_required
def add_production_entry(request):
    if request.method == 'POST':
        form = ProductionLogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('production-entry-success')
    else:
        form = ProductionLogForm()
    return render(request, 'videos/add_production_entry.html', {'form': form})

# Define a success page after adding a production entry
@login_required
def production_entry_success(request):
    return render(request, 'videos/production_entry_success.html')

# views.py

from django.shortcuts import render
from .models import Machine


@login_required
def oee_data(request):
    machines = Machine.objects.all()
    oee_data = []
    for machine in machines:
        availability = calculate_availability(machine)
        performance = calculate_performance(machine)
        quality = calculate_quality(machine)
        oee = calculate_oee(availability, performance, quality)
        oee_data.append({'machine_name': machine.machine_name, 'oee': oee})
    return render(request, 'videos/oee_data.html', {'oee_data': oee_data})

