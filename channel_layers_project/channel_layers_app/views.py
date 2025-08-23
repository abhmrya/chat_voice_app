from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from . models import Group_name, Chat_msg, OneToOneMessage, UserProfile
from django.contrib.auth.models import User
from .consumers import OneToOneAsyncConsumer
from django.db.models import Q
from django.contrib.auth.decorators import login_required


# yourapp/views.py
from rest_framework.decorators import api_view, permission_classes,APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework import permissions
from .serializers import RegisterSerializer,LoginSerializer
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import status

def register_page(request):
    return render(request,'register.html')

class  RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"user registered successfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


def login_page(request):
    return render(request, "login.html")


#login views 
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        print('------------------------------login api---------------')
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)
            # subject = "Welcome to Our Site!"
            # message = f"Hello {user.username}, thanks for login!"
            # recipient_list = [user.email]
            # send_welcome_email_task.delay(subject, message, recipient_list)  

            return Response({
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_staff": user.is_staff,
                },
                "tokens": serializer.validated_data["tokens"]
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    print("***************long out api ********************")
    try:
        # If JWT refresh token is provided, blacklist it
        refresh_token = request.data.get("refresh")

        print("**************print refresh token ****",refresh_token)
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

    # Clear Django session if exists
    request.session.flush()
    return JsonResponse({"message": "Logged out successfully"})


# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import get_object_or_404
from django.utils.timezone import now

@csrf_exempt
def upload_audio(request):
    """Save recorded voice to DB and return URL."""
    if request.method == "POST" and request.FILES.get("audio"):
        audio_file = request.FILES["audio"]
        group_name = request.POST.get("group")
        user = request.user

        group = Group_name.objects.filter(groupname=group_name).first()
        if not group:
            return JsonResponse({"error": "Group not found"}, status=400)

        chat = Chat_msg.objects.create(
            user=user,
            group=group,
            message="",   # empty msg since it's audio
            audio=audio_file,
            time=now(),
        )

        return JsonResponse({"url": chat.audio.url})

    return JsonResponse({"error": "Invalid request"}, status=400)


# Create your views here.
def index(request):

    if request.user.is_authenticated:
        print("********index*******")
        allgroup = Group_name.objects.all()
        if request.method == "POST":
            group_nm = request.POST.get('group-name')
            group = Group_name.objects.filter(groupname=group_nm).first()
            # chat_msgs = []
            if group:
                pass
            else:
                group = Group_name(groupname=group_nm)
                group.save()
        return render(request, "index.html",{'groupname':allgroup})
    else:
        return redirect("/login")

def group_chatt(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    allgroup = Group_name.objects.all()

    return render(
        request,
        "group_chat.html",{   "groupname": allgroup,}
    )


def group_chat(request, group_name):
    if not request.user.is_authenticated:
        return redirect("/login")

    allgroup = Group_name.objects.all()
    group = Group_name.objects.filter(groupname=group_name).first()
    chat_msgs = []

    if group:
        chat_msgs = Chat_msg.objects.filter(group=group).order_by("time")
    else:
        group = Group_name.objects.create(groupname=group_name)

    if request.method == "POST":
        group_nm = request.POST.get("group-name")
        Group_name.objects.get_or_create(groupname=group_nm)

    return render(
        request,
        "group_chat.html",
        {
            "group_name": group_name,
            "chat_msgs": chat_msgs,
            "groupname": allgroup,
        },
    )

def one_to_home(request):
    users = User.objects.all()
    
    return render(request, "one_to_one_home.html",{'users':users})
    

def oneto_one_chat(request):
    if request.user.is_authenticated:
        users = User.objects.all()
        user_name = None
        user = None
        chat_msgs = []
        if request.method == 'POST':
            user_name = request.POST.get('user')
            user = UserProfile.objects.filter(user__username=user_name).first()
            send_to = User.objects.filter(username=user_name).first()
            
            if send_to:
                chat_msgs = OneToOneMessage.objects.filter(
                    Q(send_from=request.user, send_to=send_to) | 
                    Q(send_from=send_to, send_to=request.user)
                ).order_by('time')

        return render(request, "one_to_one_chat.html", {
            'user_name': user_name,
            'users': users,
            'user': user,
            'chat_msgs': chat_msgs
        })
    else:
        return redirect("/login")
