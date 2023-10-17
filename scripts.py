import os
import random

import django
import click

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()


from datacenter.models import Schoolkid, Lesson, Mark, Chastisement, Commendation


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


def create_commendation(schoolkid, lesson):
    commendations = [
        'Молодец!',
        'Отлично!',
        'Хорошо!',
        'Гораздо лучше, чем я ожидал!',
        'Ты меня приятно удивил!',
        'Великолепно!',
        'Прекрасно!',
        'Ты меня очень обрадовал!',
        'Именно этого я давно ждал от тебя!',
        'Сказано здорово – просто и ясно!',
        'Ты, как всегда, точен!',
        'Очень хороший ответ!',
        'Талантливо!',
        'Ты сегодня прыгнул выше головы!',
        'Я поражен!',
        'Уже существенно лучше!',
        'Потрясающе!',
        'Замечательно',
        'Прекрасное начало!',
        'Так держать!',
        'Ты на верном пути!',
        'Здорово!',
        'Это как раз то, что нужно!',
        'Я тобой горжусь!',
        'С каждым разом у тебя получается всё лучше!',
        'Мы с тобой не зря поработали!',
        'Я вижу, как ты стараешься!',
        'Ты растешь над собой!',
        'Ты многое сделал, я это вижу!',
        'Теперь у тебя точно все получится!',
        ]

    child_lessons = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=lesson).last()
    Commendation.objects.create(
        text=random.choice(commendations),
        created=child_lessons.date,
        schoolkid=schoolkid,
        subject=child_lessons.subject,
        teacher=child_lessons.teacher)


@click.command
@click.option('--correct_grades', '-cg', is_flag=True,
              help='Correcting bad grades to "5".')
@click.option('--delete_remarks', '-dr', is_flag=True, help='Delete remarks.')
@click.option('--compliment', '-c', is_flag=True, help='Compliment.')
@click.option('--lesson', '-l', help='Identify the subject.')
@click.argument('name', required=True)
def main(name, correct_grades, delete_remarks, compliment, lesson):
    if correct_grades:
        fix_marks(get_schoolkid(name))
    elif delete_remarks:
        remove_chastisements(get_schoolkid(name))
    elif compliment:
        create_commendation(get_schoolkid(name), lesson)


if __name__ == '__main__':
    main()
