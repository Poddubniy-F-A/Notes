import csv
import datetime

PATH = 'notes.csv'

COLUMNS = ['id', 'heading', 'text', 'date']
HEADING_INDEX = COLUMNS.index('heading')
TEXT_INDEX = COLUMNS.index('text')
DATE_INDEX = COLUMNS.index('date')

DATE_AND_TIME_FORMAT = '%Y.%m.%d %H:%M:%S'
DATE_FORMAT = 'yyyy.mm.dd'
DATE_LENGTH = len(DATE_FORMAT)

identifier = 0
with open(PATH, 'r', encoding='UTF-8') as file:
    strings = list(csv.reader(file))
    if len(strings) == 0:
        with open(PATH, 'w') as f:
            csv.writer(f).writerow(COLUMNS)
    elif len(strings) > 2:
        identifier = int(strings[-2][0])


def get_cur_time():
    return datetime.datetime.now().strftime(DATE_AND_TIME_FORMAT)


def add_case():
    global identifier
    identifier += 1

    with open(PATH, 'a', encoding='UTF-8') as file:
        csv.writer(file).writerow([identifier,
                                   input('Введите заголовок: '),
                                   input('Введите заметку: '),
                                   get_cur_time()])

    print('\nЗаметка создана')


def get_notes_list():
    with open(PATH, 'r', encoding='UTF-8') as file:
        res = list(csv.reader(file))
        for i in range(res.count([])):
            res.remove([])
        return res


def overwrite_file(notes_list):
    with open(PATH, 'w') as file:
        csv.writer(file).writerows(notes_list)


def edit_note(notes, note, index):
    heading_code = '1'
    text_code = '2'
    codes = [heading_code, text_code]

    print('Возможные действия с заметкой:\n' +
          heading_code + '. Изменить заголовок\n' +
          text_code + '. Изменить текст')

    edit_var = input('Выберите нужное действие: ')
    while edit_var not in codes:
        print('Некорректный ввод')
        edit_var = input('Выберите нужное действие (' + min(codes) + '-' + max(codes) + '): ')

    if edit_var == heading_code:
        note[HEADING_INDEX] = input('Введите новый заголовок: ')
    elif edit_var == text_code:
        note[TEXT_INDEX] = input('Введите новый текст: ')
    note[DATE_INDEX] = get_cur_time()

    notes[index] = note
    overwrite_file(notes)


def edit_case():
    search = input('Введите идентификатор заметки, которую вы хотите изменить: ')
    notes = get_notes_list()

    index = 0
    for note in notes:
        if note[0] == search:
            edit_note(notes, note, index)
            print('\nЗаметка изменена')
            break
        index += 1
    else:
        print('\nЗаметки с таким идентификатором не существует')


def delete_note(notes, note):
    notes.remove(note)
    overwrite_file(notes)


def delete_case():
    search = input('Введите идентификатор заметки, которую вы хотите удалить: ')
    notes = get_notes_list()

    for note in notes:
        if note[0] == search:
            delete_note(notes, note)
            print('\nЗаметка удалена')
            break
    else:
        print('\nЗаметки с таким идентификатором не существует')


def search_case():
    search = input('Введите дату изменения нужной заметки в формате ' + DATE_FORMAT + ': ')

    search_was_successful = False
    for note in get_notes_list():
        if note[DATE_INDEX][:DATE_LENGTH] == search:
            print('{', end='')
            for i in range(len(COLUMNS) - 1):
                print('\'' + COLUMNS[i] + '\': \'' + note[i] + '\', ', sep='', end='')
            print('\'' + COLUMNS[-1] + '\': \'' + note[-1] + '\'}', sep='')
            search_was_successful = True
    if not search_was_successful:
        print('\nНичего не найдено')


def show_case():
    with open(PATH, 'r', encoding='UTF-8') as file:
        for row in csv.DictReader(file):
            print(row)


ADD_CODE = '1'
EDIT_CODE = '2'
DELETE_CODE = '3'
SEARCH_CODE = '4'
SHOW_CODE = '5'
EXIT_CODE = '6'
CODES = [ADD_CODE, EDIT_CODE, DELETE_CODE, SEARCH_CODE, SHOW_CODE, EXIT_CODE]

print('Приветствуем в Заметках!')
command = None
while command != EXIT_CODE:
    print('\nДоступные способы взаимодействия:\n' +
          ADD_CODE + '. Добавить заметку\n' +
          EDIT_CODE + '. Изменить заметку\n' +
          DELETE_CODE + '. Удалить заметку\n' +
          SEARCH_CODE + '. Найти заметку\n' +
          SHOW_CODE + '. Вывести все заметки\n' +
          EXIT_CODE + '. Выход из программы', sep='')

    command = input('Введите номер действия: ')
    while command not in CODES:
        print('\nНекорректный ввод')
        command = input('Введите номер действия (' + min(CODES) + '-' + max(CODES) + '): ')

    print()
    if command == ADD_CODE:
        add_case()
    elif command == EDIT_CODE:
        edit_case()
    elif command == DELETE_CODE:
        delete_case()
    elif command == SEARCH_CODE:
        search_case()
    elif command == SHOW_CODE:
        show_case()

print('Всего хорошего!')
