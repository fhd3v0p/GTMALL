# Generated manually for adding HTTPS image fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0005_update_product_model'),
    ]

    operations = [
        # Добавляем HTTPS поля для Artist
        migrations.AddField(
            model_name='artist',
            name='avatar_https',
            field=models.URLField(blank=True, verbose_name='HTTPS ссылка на аватар'),
        ),
        migrations.AddField(
            model_name='artist',
            name='gallery_https_1',
            field=models.URLField(blank=True, verbose_name='HTTPS ссылка на фото 1'),
        ),
        migrations.AddField(
            model_name='artist',
            name='gallery_https_2',
            field=models.URLField(blank=True, verbose_name='HTTPS ссылка на фото 2'),
        ),
        migrations.AddField(
            model_name='artist',
            name='gallery_https_3',
            field=models.URLField(blank=True, verbose_name='HTTPS ссылка на фото 3'),
        ),
        migrations.AddField(
            model_name='artist',
            name='gallery_https_4',
            field=models.URLField(blank=True, verbose_name='HTTPS ссылка на фото 4'),
        ),
        migrations.AddField(
            model_name='artist',
            name='gallery_https_5',
            field=models.URLField(blank=True, verbose_name='HTTPS ссылка на фото 5'),
        ),
        migrations.AddField(
            model_name='artist',
            name='gallery_https_6',
            field=models.URLField(blank=True, verbose_name='HTTPS ссылка на фото 6'),
        ),
        migrations.AddField(
            model_name='artist',
            name='gallery_https_7',
            field=models.URLField(blank=True, verbose_name='HTTPS ссылка на фото 7'),
        ),
        migrations.AddField(
            model_name='artist',
            name='gallery_https_8',
            field=models.URLField(blank=True, verbose_name='HTTPS ссылка на фото 8'),
        ),
        migrations.AddField(
            model_name='artist',
            name='gallery_https_9',
            field=models.URLField(blank=True, verbose_name='HTTPS ссылка на фото 9'),
        ),
        migrations.AddField(
            model_name='artist',
            name='gallery_https_10',
            field=models.URLField(blank=True, verbose_name='HTTPS ссылка на фото 10'),
        ),
        
        # Добавляем HTTPS поля для Product
        migrations.AddField(
            model_name='product',
            name='avatar_https',
            field=models.URLField(blank=True, verbose_name='HTTPS ссылка на аватар товара'),
        ),
        migrations.AddField(
            model_name='product',
            name='gallery_https_1',
            field=models.URLField(blank=True, verbose_name='HTTPS ссылка на фото товара 1'),
        ),
        migrations.AddField(
            model_name='product',
            name='gallery_https_2',
            field=models.URLField(blank=True, verbose_name='HTTPS ссылка на фото товара 2'),
        ),
        migrations.AddField(
            model_name='product',
            name='gallery_https_3',
            field=models.URLField(blank=True, verbose_name='HTTPS ссылка на фото товара 3'),
        ),
        migrations.AddField(
            model_name='product',
            name='gallery_https_4',
            field=models.URLField(blank=True, verbose_name='HTTPS ссылка на фото товара 4'),
        ),
        migrations.AddField(
            model_name='product',
            name='gallery_https_5',
            field=models.URLField(blank=True, verbose_name='HTTPS ссылка на фото товара 5'),
        ),
        migrations.AddField(
            model_name='product',
            name='gallery_https_6',
            field=models.URLField(blank=True, verbose_name='HTTPS ссылка на фото товара 6'),
        ),
        migrations.AddField(
            model_name='product',
            name='gallery_https_7',
            field=models.URLField(blank=True, verbose_name='HTTPS ссылка на фото товара 7'),
        ),
    ] 