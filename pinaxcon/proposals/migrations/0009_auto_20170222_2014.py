# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-22 09:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0008_openhardwareproposal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamesproposal',
            name='materials_release',
            field=models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any other material (such as slides) from presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"),
        ),
        migrations.AlterField(
            model_name='gamesproposal',
            name='recording_release',
            field=models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any recordings of presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"),
        ),
        migrations.AlterField(
            model_name='kernelproposal',
            name='materials_release',
            field=models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any other material (such as slides) from presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"),
        ),
        migrations.AlterField(
            model_name='kernelproposal',
            name='recording_release',
            field=models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any recordings of presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"),
        ),
        migrations.AlterField(
            model_name='knowledgeproposal',
            name='materials_release',
            field=models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any other material (such as slides) from presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"),
        ),
        migrations.AlterField(
            model_name='knowledgeproposal',
            name='recording_release',
            field=models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any recordings of presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"),
        ),
        migrations.AlterField(
            model_name='lawproposal',
            name='materials_release',
            field=models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any other material (such as slides) from presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"),
        ),
        migrations.AlterField(
            model_name='lawproposal',
            name='recording_release',
            field=models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any recordings of presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"),
        ),
        migrations.AlterField(
            model_name='openhardwareproposal',
            name='materials_release',
            field=models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any other material (such as slides) from presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"),
        ),
        migrations.AlterField(
            model_name='openhardwareproposal',
            name='recording_release',
            field=models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any recordings of presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"),
        ),
        migrations.AlterField(
            model_name='openradioproposal',
            name='materials_release',
            field=models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any other material (such as slides) from presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"),
        ),
        migrations.AlterField(
            model_name='openradioproposal',
            name='recording_release',
            field=models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any recordings of presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"),
        ),
        migrations.AlterField(
            model_name='securityproposal',
            name='materials_release',
            field=models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any other material (such as slides) from presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"),
        ),
        migrations.AlterField(
            model_name='securityproposal',
            name='recording_release',
            field=models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any recordings of presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"),
        ),
        migrations.AlterField(
            model_name='sysadminproposal',
            name='materials_release',
            field=models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any other material (such as slides) from presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"),
        ),
        migrations.AlterField(
            model_name='sysadminproposal',
            name='recording_release',
            field=models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any recordings of presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"),
        ),
        migrations.AlterField(
            model_name='talkproposal',
            name='materials_release',
            field=models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any other material (such as slides) from presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"),
        ),
        migrations.AlterField(
            model_name='talkproposal',
            name='recording_release',
            field=models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any recordings of presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"),
        ),
        migrations.AlterField(
            model_name='testingproposal',
            name='materials_release',
            field=models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any other material (such as slides) from presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"),
        ),
        migrations.AlterField(
            model_name='testingproposal',
            name='recording_release',
            field=models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any recordings of presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"),
        ),
        migrations.AlterField(
            model_name='tutorialproposal',
            name='materials_release',
            field=models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any other material (such as slides) from presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"),
        ),
        migrations.AlterField(
            model_name='tutorialproposal',
            name='recording_release',
            field=models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any recordings of presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"),
        ),
        migrations.AlterField(
            model_name='wootconfproposal',
            name='materials_release',
            field=models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any other material (such as slides) from presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"),
        ),
        migrations.AlterField(
            model_name='wootconfproposal',
            name='recording_release',
            field=models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any recordings of presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"),
        ),
        migrations.AlterField(
            model_name='writethedocsproposal',
            name='materials_release',
            field=models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any other material (such as slides) from presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"),
        ),
        migrations.AlterField(
            model_name='writethedocsproposal',
            name='recording_release',
            field=models.BooleanField(default=True, help_text=b"I allow PyCon Australia to release any recordings of presentations covered by this proposal, under the <a href='https://creativecommons.org/licenses/by-sa/3.0/au/deed.en'> Creative Commons Attribution-Share Alike Australia 3.0 Licence</a>"),
        ),
    ]
