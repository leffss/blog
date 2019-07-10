# Generated by Django 2.2.3 on 2019-07-09 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_auto_20190626_1541'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': '文章分类', 'verbose_name_plural': '文章分类'},
        ),
        migrations.AlterModelOptions(
            name='series',
            options={'verbose_name': '文章系列', 'verbose_name_plural': '文章系列'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': '文章标签', 'verbose_name_plural': '文章标签'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=32, unique=True, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=32, unique=True, verbose_name='名称'),
        ),
    ]
