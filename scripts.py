import argparse
import os
import random
import sys

import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()


from datacenter.models import Schoolkid, Lesson, Mark, Chastisement, Commendation


COMMENDATIONS = [
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


def get_schoolkid(child):
    if not child:
        print('Имя ученика не указано')
        sys.exit()
    else:
        try:
            schoolkid = Schoolkid.objects.get(full_name__contains=child)
            return schoolkid
        except Schoolkid.DoesNotExist:
            print('Ученик не найден в базе данных')
            sys.exit()
        except Schoolkid.MultipleObjectsReturned:
            print('Найдено более одного ученика')
            sys.exit()


def fix_marks(schoolkid):
    child_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    child_marks.update(points=5)


def remove_chastisements(schoolkid):
    child_chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    child_chastisements.delete()


def create_commendation(schoolkid, lesson):
    try:
        child_lessons = Lesson.objects.filter(
            year_of_study=schoolkid.year_of_study,
            group_letter=schoolkid.group_letter,
            subject__title=lesson).last()
        Commendation.objects.create(
            text=random.choice(COMMENDATIONS),
            created=child_lessons.date,
            schoolkid=schoolkid,
            subject=child_lessons.subject,
            teacher=child_lessons.teacher)
    except AttributeError:
        print('Предмет указан некорректно, введите правильное название предмета.')


def main():
    parser = argparse.ArgumentParser(
        description='Скрипты для электронного дневника'
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
