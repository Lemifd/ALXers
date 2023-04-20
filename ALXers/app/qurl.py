from django.urls import path
from . import views

urlpatterns = [
    path("",views.problems),
    path('<int:id>/',views.questions),

]

