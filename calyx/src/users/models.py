from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

if TYPE_CHECKING:
    from courses.models import Course


class StudentNumberValidator(ASCIIUsernameValidator):
    regex = r'^[bmd]\d{7}$'
    message = 'Enter a valid student number. For example, b1234567 or m7654321.'


class UserManager(BaseUserManager):
    """
    カスタムユーザモデルのためのマネージャ
    """

    def __init__(self, alive_only: bool = True, *args, **kwargs):
        self.alive_only = alive_only
        super(UserManager, self).__init__(*args, **kwargs)

    def create_user(self, username, password, **extra_fields):
        """
        ユーザ作成の関数
        :param username: 学生ID b0000000 *必須*
        :param password: パスワード
        :param extra_fields: その他のパラメータ
        :return: 作成されたStudentのインスタンス
        """
        if not username:
            return ValueError('Student number is required')
        student = self.model(
            username=username,
            email=username + '@' + settings.STUDENT_EMAIL_DOMAIN,  # メールアドレスを動的に生成
            **extra_fields
        )
        student.set_password(password)
        student.save(using=self.db)
        return student

    def create_superuser(self, username, password, **kwargs):
        """
        /adminにログインできるスーパーユーザ作成用の関数
        :param username: 学生ID *必須*
        :param password: パスワード
        :return: 作成されたStudentのインスタンス
        """
        return self.create_user(username=username, password=password, is_staff=True,
                                is_superuser=True, is_active=True, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    """
    学生のモデル
    """
    # ユーザ名をバリデーション
    username_validator = StudentNumberValidator()

    username = models.CharField(max_length=64, unique=True, verbose_name='学生ID',
                                help_text='小文字の英数字および数字のみ使用できます',
                                validators=[username_validator])
    email = models.EmailField(max_length=255, unique=True, default='')
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField('登録日時', auto_now_add=True)
    modified_at = models.DateTimeField('更新日時', auto_now=True)

    screen_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='氏名')
    gpa = models.FloatField(verbose_name='GPA', blank=True, null=True,
                            validators=[MinValueValidator(0.0), MaxValueValidator(4.0)])

    # ユーザ名のフィールドを学生IDに設定
    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        """学生IDを返却"""
        return self.username

    class Meta:
        ordering = ['username']
        verbose_name = '学生'
        verbose_name_plural = '学生'
