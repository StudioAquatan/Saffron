from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, mixins, serializers, status, exceptions
from rest_framework.response import Response

from courses.errors import NotJoinedError, NotAdminError
from courses.models import Course
from courses.permissions import (
    IsAdmin, IsCourseMember, IsCourseAdmin
)
from courses.serializers import (
    ReadOnlyCourseSerializer, JoinSerializer, UserSerializer, CourseStatusSerializer
)
from .mixins import CourseNestedMixin

User = get_user_model()


class JoinAPIView(CourseNestedMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    課程に参加するAPIビュー

    create:
        課程に参加する
    """
    queryset = Course.objects.prefetch_related(
        Prefetch('users', User.objects.prefetch_related('groups', 'courses').all()),
    ).select_related('admin_user_group', 'year').all()
    serializer_class = JoinSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=JoinSerializer,
        responses={
            200: ReadOnlyCourseSerializer,
            400: "PINコードが正しくない，または既に参加済みです",
            401: "ログインしてください",
            404: "指定された課程は存在しません",
        }
    )
    def create(self, request, course_pk=None, *args, **kwargs):
        course = self.get_course()
        # PINコードをパース
        pin_code_serializer = self.get_serializer(instance=course, data=request.data)
        pin_code_serializer.is_valid(raise_exception=True)
        course = pin_code_serializer.save()
        course_serializer = ReadOnlyCourseSerializer(course, context=self.get_serializer_context())
        headers = self.get_success_headers(course_serializer.data)
        return Response(course_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CourseAdminView(CourseNestedMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """
    各課程の管理者に関するView
    update:
        IDを指定して管理者でないユーザを管理者に昇格する
    partial_update:
        IDを指定して管理者でないユーザを管理者に昇格する
    list:
        管理者一覧を表示する
    destroy:
        IDを指定して管理者から外す
    """

    queryset = Course.objects.prefetch_related(
        Prefetch('users', User.objects.prefetch_related('groups', 'courses').all()),
    ).select_related('admin_user_group', 'year')
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [IsCourseMember | IsAdmin]
        else:
            self.permission_classes = [(IsCourseMember & IsCourseAdmin) | IsAdmin]
        return super(CourseAdminView, self).get_permissions()

    def update(self, request, *args, **kwargs):
        pk = kwargs.pop('pk')
        if not isinstance(pk, int):
            pk = int(pk)
        course = self.get_course()
        try:
            user = course.users.get(pk=pk)
        except User.DoesNotExist:
            raise exceptions.NotFound('指定されたユーザはこの課程に参加していないか，存在しません．')
        try:
            if user.groups.filter(name=course.admin_group_name).exists():
                raise serializers.ValidationError({'non_field_errors': 'このユーザは既に管理者として登録されています．'})
            course.register_as_admin(user)
        except NotJoinedError:
            raise serializers.ValidationError({'non_field_errors': 'このユーザはこの課程のメンバーではありません'})
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.pop('pk')
        if not isinstance(pk, int):
            pk = int(pk)
        course = self.get_course()
        if request.user.pk == pk:
            raise serializers.ValidationError({'non_field_errors': '自分自身を管理者から外すことは出来ません．'})
        try:
            user = course.users.get(pk=pk)
        except User.DoesNotExist:
            raise exceptions.NotFound('指定されたユーザはこの課程に参加していないか，存在しません．')
        try:
            course.unregister_from_admin(user)
        except NotAdminError:
            raise serializers.ValidationError({'non_field_errors': 'このユーザは管理者として登録されていません．'})
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        course = self.get_course()
        admins = course.users.filter(groups__name=course.admin_group_name).all()
        serializer = self.get_serializer(admins, many=True)
        return Response(serializer.data)


class RequirementStatusView(CourseNestedMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    課程の設定と照らし合わせてそのユーザが要求を満たしているかどうかをチェックするビュー

    list:
        要求を満たしているかどうかの状態を取得する
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CourseStatusSerializer

    @swagger_auto_schema(responses={
        200: CourseStatusSerializer,
        401: "ログインしていません",
        403: "課程に参加していません",
        404: "指定した課程は存在しません"
    })
    def list(self, request, **kwargs):
        course = self.get_course()
        serializer_context = self.get_serializer_context()
        serializer_context['course_pk'] = course.pk
        serializer = CourseStatusSerializer(instance=request.user, context=serializer_context)
        return Response(serializer.data)
