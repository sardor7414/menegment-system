from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    CreateAPIView, ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveDestroyAPIView
)
from .models import Board, Column, Task, BoardMember
from .serializers import (
    BoardSerializer, ColumnSerializer, UserRegisterSerializer, TaskSerializer,
    BoardDataSerializer, ShareBoardSerializer, VerifyCodeSerializer
)

from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView

from v1.user.models import User


# Create your views here.
class VerifyCode(APIView):

    def post(self, request):
        data = request.data
        token = data.get('token')
        code = data.get('code')
        if not code or not token:
            return Response({"error": "Token or code not given"})
        board_member = BoardMember.objects.filter(
            is_success=False, token=token, code=code
        ).first()
        if board_member:
            board_member.is_success = True
            board_member.save()
            return Response({"status": True})
        return Response({"status": False})


# These functions are working properly

class UserRegisterAPI(APIView):

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ShareBoard(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ShareBoardSerializer

    def perform_create(self, serializer):
        return serializer.save(inviter_id=self.request.user.id)


class GetBoardDataAPI(ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardDataSerializer
    pagination_class = None

    def get_queryset(self):
        params = self.request.query_params
        board_id = params.get('board_id')
        if not board_id:
            return
        queryset = super().get_queryset().filter(id=board_id, user_id=self.request.user.id).first()
        if not queryset:
            return
        return queryset.board_columns.all()


class BoardCreateAPI(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(user_id=self.request.user.id) | Q(board_member__user_id=self.request.user.id))


class UpdateBoardAPI(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class TaskCreateAPI(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskEditAPI(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
