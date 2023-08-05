# Generated by Django 3.2.20 on 2023-08-03 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20230801_0516'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
        migrations.AddField(
            model_name='product',
            name='article',
            field=models.IntegerField(default=1, verbose_name='Артикл'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='link',
            field=models.CharField(max_length=1024, verbose_name='Ссылка'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(verbose_name='Цена'),
        ),
    ]
