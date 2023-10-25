from rest_framework import serializers
from .models import Board, Column, Task, BoardMember
from v1.user.models import User
from v1.user.serializers import UserSerializer
from ..services import send_message_to_email
from rest_framework.response import Response
import random, uuid
from django.db import transaction



class UserRegisterSerializer(serializers.ModelSerializer):
    reply_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone', 'password', 'reply_password')

    def validate(self, attrs):
        attrs = super().validate(attrs)
        phone = attrs['phone']
        user = User.objects.filter(phone=phone).first()
        if user:
            return serializers.ValidationError("User registered with this phone number")
        password = attrs['password']
        reply_password = attrs.pop('reply_password')
        if password != reply_password:
            return serializers.ValidationError("Passwords don't match")
        return attrs


# Verify code serializer
class VerifyCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardMember
        fields = ('code', )

    def validate(self, attrs):
        res = super().validate(attrs)
        incaming_code = res['code']
        code = BoardMember.objects.filter(code=incaming_code, is_succes=False).first()
        if not code:
            return Response({"message": "Code doesn't exists"})
        return res



class ShareBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardMember
        fields = ('id', 'user', 'board')

    def validate(self, attrs):
        res = super().validate(attrs)
        board = res['board']
        user = self.context['request'].user
        board_room = BoardMember.objects.filter(board_id=board.id, user_id=user.id).first()
        if board.user.id == user.id or board_room:
            return res
        return serializers.ValidationError("Board not Found")

    def create(self, validated_data):
        with transaction.atomic():
            code = random.randint(1000, 9999)
            token = uuid.uuid4()
            data = {
                "code": code,
                "token": token
            }
            obj = self.Meta.model.objects.create(**validated_data, **data)
            send_message_to_email(obj.user.email, obj.inviter.email, code, token)
        return obj

    def to_representation(self, instance):
        res = {
            "statue": True,
            "message": "We have sent code to email"
        }
        return res




class BoardDataSerializer(serializers.Serializer):
    columns = serializers.SerializerMethodField()
    tasks = serializers.SerializerMethodField()

    def get_columns(self, instance):
        return {
            'id': instance.id,
            'title': instance.title
        }

    def get_tasks(self, instance):
        return TaskGetSerializer(instance.column_tasks.all(), many=True).data


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ('id', 'title')


class BoardSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    columns = serializers.ListField(write_only=True)
    board_members = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ('id', 'title', 'description', 'user', 'board_members', 'columns')

    def get_user(self, instance):
        return {
            'id': instance.user.id,
            'phone': instance.user.phone
        }

    def create(self, validated_data):
        columns = validated_data.pop('columns')
        board = super().create(validated_data)
        column_list = []
        for column in columns:
            column_list.append(
                Column(title=column, board=board)
            )
            # Column.objects.create(title=column, board=board)
        if column_list:
            Column.objects.bulk_create(column_list)
        return board

    def get_board_members(self, instance):
        members = User.objects.filter(board_member__board_id=instance.id)
        serializer = UserSerializer(members, many=True)
        return serializer.data

    def to_representation(self, instance):
        res = super().to_representation(instance)
        columns = Column.objects.select_related("board").filter(board_id=instance.id)
        res['columns'] = ColumnSerializer(columns, many=True).data
        return res



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'column')

    def validate(self, attrs):
        res = super().validate(attrs) 
        column = res['column']
        user = self.context['request'].user
        if column.board.user.id != user.id:
            raise serializers.ValidationError("Column id not found")
        return res



class TaskGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description')


