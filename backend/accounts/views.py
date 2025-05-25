import requests
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from .models import User
from .serializers import UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])

def google_login(request):
    """
    接收前端傳來的 Google ID token，驗證並登入用戶
    """
    id_token = request.data.get('id_token')
    
    if not id_token:
        return Response({"error": "ID token 未提供"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # 使用 Google API 客戶端庫驗證 ID token
        # 需要先安裝: pip install google-auth
        from google.oauth2 import id_token as google_id_token
        from google.auth.transport import requests
        
        # 驗證 ID token
        idinfo = google_id_token.verify_oauth2_token(
            id_token, requests.Request(), settings.GOOGLE_CLIENT_ID, clock_skew_in_seconds=60)
        
        # 確保這是來自 Google 的 token
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('錯誤的 token 發行者')
        
        # 從已驗證的 token 中獲取用戶信息
        google_id = idinfo['sub']
        email = idinfo['email']
        name = idinfo.get('name', '')
        picture = idinfo.get('picture', '')
        
        # 處理用戶（創建或獲取）
        user = process_google_user({
            'sub': google_id,
            'email': email,
            'name': name,
            'picture': picture
        })
        
        # 生成 JWT Token
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

def process_google_user(user_info):
    """
    處理 Google 用戶 - 如果存在則返回，否則創建新用戶
    """
    google_id = user_info.get('sub')
    email = user_info.get('email')
    name = user_info.get('name', '')
    picture = user_info.get('picture', '')
    
    # 查找現有用戶
    try:
        user = User.objects.get(google_id=google_id)
        return user
    except User.DoesNotExist:
        pass
    
    # 查找是否有相同 email 的用戶
    try:
        user = User.objects.get(email=email)
        # 更新 Google ID
        user.google_id = google_id
        if picture:
            user.profile_image = picture
        user.save()
        return user
    except User.DoesNotExist:
        pass
    
    # 創建新用戶
    username = email.split('@')[0]
    # 確保用戶名唯一
    base_username = username
    i = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}_{i}"
        i += 1
    
    user = User.objects.create(
        username=username,
        email=email,
        google_id=google_id,
        profile_image=picture,
        first_name=name.split(' ')[0] if name else '',
        last_name=' '.join(name.split(' ')[1:]) if name and ' ' in name else ''
    )
    user.set_unusable_password()  # 設置不可用密碼，因為使用 Google 登入
    user.save()
    
    return user

@api_view(['GET'])
def get_user_info(request):
    """
    獲取當前登入用戶的信息
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)