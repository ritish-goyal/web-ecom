# Generated by Django 4.2.2 on 2023-07-20 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0004_alter_voter_election'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='voter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voter', to='clubs.clubmember'),
        ),
    ]
