import argparse
import os
import random

import django


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


def main():
    parser = argparse.ArgumentParser(
        description='Скрипты для электроноого дневника'
        )
    parser.add_argument(
        'script',
        help='Действие: fix_marks, remove_chastisements, create_commendation'
        )
    parser.add_argument('name', help='Имя ученика')
    parser.add_argument('--lesson', help='Урок для похвалы')
    args = parser.parse_args()

    if args.script == 'fix_marks':
        fix_marks(get_schoolkid(args.name))
    elif args.script == 'remove_chastisements':
        remove_chastisements(get_schoolkid(args.name))
    elif args.script == 'create_commendation':
        create_commendation(get_schoolkid(args.name), args.lesson)


if __name__ == '__main__':
    main()
