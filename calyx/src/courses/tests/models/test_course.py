from datetime import datetime

from django.db import IntegrityError
from django.test import TestCase

from courses.errors import NotJoinedError, AlreadyJoinedError, NotAdminError
from courses.models import Course, Year
from courses.tests.base import DatasetMixin
from users.models import User


class CourseTest(DatasetMixin, TestCase):

    def test_create_course(self):
        """課程を作成する"""
        name = self.course_data_set[0]['name']
        year_int = self.course_data_set[0]['year']
        course = Course.objects.create_course(**self.course_data_set[0])
        year = Year.objects.filter(year=year_int).first()
        self.assertEqual(name, course.name)
        self.assertEqual(year_int, year.year)
        self.assertNotEqual(self.course_data_set[0]['pin_code'], course.pin_code)

    def test_create_course_without_year(self):
        """明示的にyearを与えずに課程を作成する"""
        year_int = datetime.now().year
        name = self.course_data_set[1]['name']
        course = Course.objects.create_course(**self.course_data_set[1])
        year = Year.objects.filter(year=year_int).first()
        self.assertEqual(name, course.name)
        self.assertEqual(year_int, year.year)
        self.assertNotEqual(self.course_data_set[1]['pin_code'], course.pin_code)

    def test_create_duplicate_course(self):
        """同じ名前の課程を作成する"""
        # 同じ年度
        Course.objects.create_course(**self.course_data_set[0])
        with self.subTest(duplicate=True):
            with self.assertRaises(IntegrityError):
                Course.objects.create_course(**self.course_data_set[0])
        # 別の年度
        y = 1999
        Course.objects.create_course(**self.course_data_set[1], year=y)
        Course.objects.create_course(**self.course_data_set[1])
        with self.subTest(duplicate=False):
            self.assertEqual(3, len(Year.objects.all()))

    def test_authenticate(self):
        """課程へ設定されているPINコードで認証する"""
        raw_pin_code = self.course_data_set[0]['pin_code']
        course = Course.objects.create_course(**self.course_data_set[0])
        # 異なるパスワードで認証
        with self.subTest(truth=raw_pin_code, actual="piyo"):
            self.assertFalse(course.check_password("piyo"))
        # 正しいパスワードで認証
        with self.subTest(truth=raw_pin_code, actual=raw_pin_code):
            self.assertTrue(course.check_password(raw_pin_code))

    def test_add_users(self):
        """課程にユーザをジョインさせる"""
        course = Course.objects.create_course(**self.course_data_set[0])
        raw_pin_code = self.course_data_set[0]['pin_code']
        users = [User.objects.create_user(**user_data) for user_data in self.user_data_set]
        for user in users:
            with self.subTest(user=user):
                self.assertTrue(course.join(user, raw_pin_code))
        # course = Course.objects.get(course.pk)
        with self.subTest():
            self.assertEqual(len(self.user_data_set), len(course.users.all()))

    def test_add_joined_user(self):
        """参加済みの課程にユーザをジョインさせる"""
        course_data = self.course_data_set[0]
        pin_code = course_data['pin_code']
        course = Course.objects.create_course(**course_data)
        user = User.objects.create_user(**self.user_data_set[0])
        self.assertTrue(course.join(user, pin_code))
        with self.assertRaises(AlreadyJoinedError):
            course.join(user, pin_code)

    def test_register_as_admin(self):
        """ユーザを管理者として登録する"""
        course_data = self.course_data_set[0]
        raw_pin_code = course_data['pin_code']
        course = Course.objects.create_course(**course_data)
        users = [User.objects.create_user(**user_data) for user_data in self.user_data_set]
        for user in users:
            with self.subTest(joined=True):
                with self.assertRaises(NotJoinedError):
                    course.register_as_admin(user)
            with self.subTest(joined=False):
                self.assertTrue(course.join(user, raw_pin_code))
                self.assertEqual(None, course.register_as_admin(user))

    def test_unregister_from_admin(self):
        """ユーザを管理者から外す"""
        course_data = self.course_data_set[0]
        raw_pin_code = course_data['pin_code']
        course = Course.objects.create_course(**course_data)
        users = [User.objects.create_user(**user_data) for user_data in self.user_data_set]
        for user in users:
            with self.subTest():
                self.assertTrue(course.join(user, raw_pin_code))
                self.assertEqual(None, course.register_as_admin(user))
                self.assertEqual(None, course.unregister_from_admin(user))
                with self.assertRaises(NotAdminError):
                    course.unregister_from_admin(user)

    def test_leave_user(self):
        """課程からユーザが抜ける"""
        course = Course.objects.create_course(**self.course_data_set[0])
        users = [User.objects.create_user(**user_data) for user_data in self.user_data_set]
        for user in users:
            with self.subTest(user=user, leave=False):
                self.assertTrue(course.join(user, self.course_data_set[0]['pin_code']))
        for user in users:
            with self.subTest(user=user, leave=True):
                self.assertEqual(None, course.leave(user))
        self.assertEqual(0, len(course.users.all()))

    def test_leave_not_joined_user(self):
        """どの課程にも所属していないユーザが抜ける"""
        course = Course.objects.create_course(**self.course_data_set[0])
        user = User.objects.create_user(**self.user_data_set[0])
        with self.assertRaises(NotJoinedError):
            course.leave(user)

    def test_update_pin_code(self):
        """課程のpin_codeを更新する"""
        course = Course.objects.create_course(**self.course_data_set[0])
        old_pin_code = self.course_data_set[0]['pin_code']
        new_pin_code = "abcd"
        course.set_password(new_pin_code)
        course.save()
        user = User.objects.create_user(**self.user_data_set[0])
        # 古いpin_codeでは参加できない
        with self.subTest(truth=new_pin_code, actual=old_pin_code):
            self.assertFalse(course.join(user, old_pin_code))
        # 新しいpin_codeでは参加できる
        with self.subTest(truth=new_pin_code, actual=new_pin_code):
            self.assertTrue(course.join(user, new_pin_code))

    def test_delete_course(self):
        """課程を消去する"""
        course = Course.objects.create_course(**self.course_data_set[0])
        users = [User.objects.create_user(**user_data) for user_data in self.user_data_set]
        for user in users:
            with self.subTest(user=user):
                self.assertTrue(course.join(user, self.course_data_set[0]['pin_code']))
        course.delete()
        self.assertEqual(0, Course.objects.count())
        self.assertEqual(1, Year.objects.count())
        for user in users:
            with self.subTest(user=user):
                courses = user.courses.all()
                self.assertEqual(0, len(courses))

    def test_change_group_name(self):
        """課程名を変更したときに自動でグループ名を変更する"""
        course = Course.objects.create_course(**self.course_data_set[0])
        course.name = "updated"
        course.save()
        # グループの変更を再取得
        course = Course.objects.get(pk=course.pk)
        self.assertEqual(course.admin_group_name, course.admin_user_group.name)
