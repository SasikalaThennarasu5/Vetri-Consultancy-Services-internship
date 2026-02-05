from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("profile/", include("profiles.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),  # 👈 THIS LINE
    path("accounts/", include("allauth.urls")), 
    path('', include('jobs.urls')),
    path('auth/', include('profiles.urls')),
    path('dashboard/', include('dashboard.urls')),
    path("training/", include("training.urls")),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("chatbot/", include("chatbot.urls")),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)