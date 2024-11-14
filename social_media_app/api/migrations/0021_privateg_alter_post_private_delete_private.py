# Generated by Django 5.1.3 on 2024-11-13 15:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_alter_private_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateG',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=8)),
                ('members', models.ManyToManyField(blank=True, related_name='private_members', to='api.account')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='private_group', to='api.account')),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='private',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='api.privateg'),
        ),
        migrations.DeleteModel(
            name='Private',
        ),
    ]
