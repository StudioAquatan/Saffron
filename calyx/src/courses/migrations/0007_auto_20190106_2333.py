# Generated by Django 2.1.5 on 2019-01-06 14:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0006_auto_20190106_1927'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(verbose_name='志望順位')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='課程')),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Lab', verbose_name='研究室')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザ')),
            ],
            options={
                'verbose_name': '志望順位',
                'verbose_name_plural': '志望順位',
            },
        ),
        migrations.AddField(
            model_name='config',
            name='rank_limit',
            field=models.IntegerField(default=3, verbose_name='表示する志望順位の数'),
        ),
        migrations.AlterUniqueTogether(
            name='rank',
            unique_together={('user', 'order', 'course')},
        ),
    ]
