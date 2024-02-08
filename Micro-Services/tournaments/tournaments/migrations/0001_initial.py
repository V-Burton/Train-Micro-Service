# Generated by Django 5.0.1 on 2024-01-24 04:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('max_players', models.IntegerField()),
                ('status', models.CharField(choices=[('open', 'Open'), ('in progress', 'In Progress'), ('completed', 'Completed')], max_length=50)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TournamentParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('active', 'Active'), ('eliminated', 'Eliminated')], max_length=50)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='tournaments.tournament')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tournament_participations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('tournament', 'user')},
            },
        ),
    ]
