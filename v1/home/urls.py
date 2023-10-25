from django.urls import path
from .views import (
    BoardCreateAPI, TaskEditAPI, UpdateBoardAPI, TaskCreateAPI, UserRegisterAPI,
    GetBoardDataAPI, ShareBoard, VerifyCode
)

urlpatterns = [
    path('verify/', VerifyCode.as_view()),

    path('register/', UserRegisterAPI.as_view()),
    path('share/', ShareBoard.as_view()),
    path('task/detail/<int:pk>/', TaskEditAPI.as_view()),
    path('get/board-data/', GetBoardDataAPI.as_view()),
    path('create-board/', BoardCreateAPI.as_view()),
    path('update-board/<int:pk>/', UpdateBoardAPI.as_view()),
    path('create-task/', TaskCreateAPI.as_view())
]