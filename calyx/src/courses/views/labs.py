from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, exceptions
from rest_framework.response import Response

from courses.models import Course, Lab
from courses.permissions import (
    IsAdmin, IsCourseMember, IsCourseAdmin, GPARequirement, ScreenNameRequirement, RankSubmitted
)
from courses.schemas import LabSchema
from courses.serializers import (
    LabSerializer, LabAbstractSerializer
)
from .mixins import NestedViewSetMixin

User = get_user_model()


class LabViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    研究室を操作するView．
    """

    queryset = Lab.objects.select_related('course').all()
    schema = LabSchema()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'create':
            return LabAbstractSerializer
        return LabSerializer

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = [IsCourseMember | IsAdmin]
        elif self.action == "retrieve":
            self.permission_classes = [(IsCourseMember & GPARequirement &
                                        ScreenNameRequirement & RankSubmitted) | IsAdmin]
        else:
            self.permission_classes = [(IsCourseMember & IsCourseAdmin) | IsAdmin]
        return super(LabViewSet, self).get_permissions()

    def list(self, request, *args, **kwargs):
        course_pk = kwargs.pop('course_pk')
        try:
            self.course = Course.objects.prefetch_related('users').select_related('year').get(pk=course_pk)
        except Course.DoesNotExist:
            raise exceptions.NotFound('この課程は存在しません．')
        self.check_object_permissions(request, self.course)
        return super(LabViewSet, self).list(request, *args, **kwargs)

    def get_object(self):
        pk = self.kwargs.pop('pk')
        course_pk = self.kwargs.get('course_pk', None)
        try:
            obj = Lab.objects.filter(course_id=course_pk).select_related('course').get(pk=pk)
        except Lab.DoesNotExist:
            raise exceptions.NotFound('見つかりませんでした．')
        self.check_object_permissions(self.request, obj.course)
        self.course = obj.course
        return obj

    def get_serializer_context(self):
        context = super(LabViewSet, self).get_serializer_context()
        if hasattr(self, 'course'):
            context['course'] = self.course
        return context

    @swagger_auto_schema(
        request_body=LabAbstractSerializer(many=True),
        responses={
            201: LabAbstractSerializer(many=True),
            400: 'Validation error',
            403: 'ログインしていない，またはこの課程に参加していません'
        }
    )
    def create(self, request, *args, **kwargs):
        course_pk = kwargs.pop('course_pk')
        try:
            self.course = Course.objects.prefetch_related('users').select_related('year').get(pk=course_pk)
        except Course.DoesNotExist:
            raise exceptions.NotFound('この課程は存在しません．')
        self.check_object_permissions(request, self.course)
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
