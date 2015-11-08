# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('start', models.DateTimeField(auto_now_add=True)),
                ('end', models.DateTimeField(null=True, blank=True)),
                ('observers', models.ManyToManyField(related_name='meetings_as_observer', to=settings.AUTH_USER_MODEL, blank=True)),
                ('voters', models.ManyToManyField(related_name='meetings_as_voter', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('start', models.DateTimeField(auto_now_add=True)),
                ('end', models.DateTimeField(null=True, blank=True)),
                ('meeting', models.ForeignKey(related_name='tickets', to='censeo.Meeting')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('story_point', models.FloatField(choices=[(0.0, '0'), (0.5, '1/2'), (1.0, '1'), (2.0, '2'), (3.0, '3'), (5.0, '5'), (8.0, '8'), (13.0, '13'), (20.0, '20'), (40.0, '40'), (100.0, '100')])),
                ('ticket', models.ForeignKey(related_name='ticket_votes', to='censeo.Ticket')),
                ('user', models.ForeignKey(related_name='user_votes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('user', 'ticket')]),
        ),
    ]
