# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0002_factura_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='date',
            field=models.DateField(),
        ),
    ]
