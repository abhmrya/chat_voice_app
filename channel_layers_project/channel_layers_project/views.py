from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import redirect
# from django.contrib.auth.views import l


def google_login_jwt_token(request):

    print("---------google login-------")
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    refresh = RefreshToken.for_user(request.user)
    # Store tokens in session or pass as query params to your frontend
    request.session['access'] = str(refresh.access_token)
    request.session['refresh'] = str(refresh)
    
    return redirect('/index/')  # or wherever your base.html loads

# from rest_framework_simplejwt.tokens import RefreshToken
# from django.shortcuts import redirect

# def google_login_jwt_token(request):
#     print("--------------------------------")
#     if not request.user.is_authenticated:
#         return redirect('/login/')
    
#     # Generate JWT for the logged-in user
#     refresh = RefreshToken.for_user(request.user)
    
#     # Save in session (optional, if you want server-side)
#     request.session['access'] = str(refresh.access_token)
#     request.session['refresh'] = str(refresh)

#     # Redirect to base.html and pass tokens via query params
#     return redirect(f"/base/?access={refresh.access_token}&refresh={refresh}")
