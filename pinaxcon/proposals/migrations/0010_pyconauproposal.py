# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-12 23:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('symposion_proposals', '0001_initial'),
        ('symposion_conference', '0001_initial'),
        ('proposals', '0009_auto_20170222_2014'),
    ]

    operations = [
        migrations.CreateModel(
            name='PyConAuProposal',
            fields=[
                ('proposalbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='symposion_proposals.ProposalBase')),
                ('target_audience', models.IntegerField(choices=[(1, b'User'), (2, b'Business'), (3, b'Community'), (4, b'Developer')])),
                ('recording_release', models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any recordings of presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>")),
                ('materials_release', models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any other material (such as slides) from presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>")),
                ('length', models.IntegerField(choices=[(1, b'Short presentation (30mins)'), (2, b'Long presentation (70mins)')], help_text=b'Please select the desired length of your presentation. The paper committee may ask you to reconsider your desired length.')),
                ('area', models.ManyToManyField(help_text=b'Please select the areas of the conference that you think your talk is applicable to. The paper committee may ask you to reconsider your desired areas.', to='symposion_conference.Section')),
            ],
            options={
                'verbose_name': 'PyCon Australia talk proposal',
            },
            bases=('symposion_proposals.proposalbase',),
        ),
    ]
