import os

import django
import click

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()


from datacenter.models import Schoolkid, Mark, Chastisement


def get_schoolkid(child):
    schoolkid = Schoolkid.objects.get(full_name__contains=child)
    return schoolkid


def fix_marks(schoolkid):
    child_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    for mark in child_marks:
        mark.points = 5
        mark.save()


def remove_chastisements(schoolkid):
    child_chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    child_chastisements.delete()


@click.command
@click.option('--correct_grades', '-cg', is_flag=True,
              help='Correcting bad grades to "5".')
@click.option('--delete_remarks', '-dr', is_flag=True, help='Delete remarks.')
@click.argument('name', required=True)
def main(name, correct_grades, delete_remarks):
    if correct_grades:
        fix_marks(get_schoolkid(name))
    elif delete_remarks:
        remove_chastisements(get_schoolkid(name))


if __name__ == '__main__':
    main()
