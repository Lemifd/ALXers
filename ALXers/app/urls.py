from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("",views.home),
    path('home/',views.home),
    path('register/',views.register),
    path('profile/',views.profile),
    path('signin/', views.signin),
    path('problems/',include('app.qurl')),
    path('logout/',views.logout),
    path('add/',views.add),
    path('uploads/',views.add),
]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

