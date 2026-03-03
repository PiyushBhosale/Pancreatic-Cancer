import tensorflow as tf
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Prediction
from .serializers import PredictionSerializer, PredictionResultSerializer, UserSerializer
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return 
    
@ensure_csrf_cookie
def get_csrf(request):
    return JsonResponse({"message": "CSRF cookie set"})

MODEL_PATH = os.path.join(
    settings.BASE_DIR,
    "API",
    "assests",
    "CancerModel.keras"
)
model = tf.keras.models.load_model(MODEL_PATH)


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return []  # Allow anyone to register
        return [permissions.IsAuthenticated()]


class PredictionViewSet(viewsets.ModelViewSet):

    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Prediction.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            # Save uploaded image first
            prediction_obj = serializer.save(user=request.user)

            # Get image path from model
            image_path = prediction_obj.uploaded_image.path

            #  Step 1: Read image
            image = tf.io.read_file(image_path)

            #  Step 2: Decode image
            image = tf.image.decode_jpeg(image, channels=3)

            #  Step 3: Resize (use SAME size as training)
            image = tf.image.resize(image, [244, 244])

            #  Step 4: Normalize
            image = tf.cast(image / 255.0, tf.float32)

            #  Step 5: Add batch dimension
            input_image = tf.expand_dims(image, axis=0)

            #  Step 6: Predict
            prediction = model.predict(input_image)

            confidence = float(prediction[0][0])
            confidence_percent = confidence * 100

            #  Binary Classification Logic
            if confidence >= 0.5:
                label = "Cancer"
            else:
                label = "No Cancer"

            # Save results
            prediction_obj.predicted_label = label
            prediction_obj.confidence_score = confidence_percent
            prediction_obj.save()

            response_serializer = PredictionResultSerializer(prediction_obj)

            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@csrf_exempt
def signup_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return JsonResponse({"message": "User created successfully"}, status=200)


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("username")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"redirect": "http://127.0.0.1:5500/Frontend/home.html"})
        else:
            return JsonResponse({"error": "Invalid username or password"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"message": "Logged out successfully"})


@login_required
def check_auth_view(request):
    return JsonResponse({"message": "Authenticated"})