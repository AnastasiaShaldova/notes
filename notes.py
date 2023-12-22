import argparse
import json
from datetime import datetime


class NoteManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.notes = []
        self.load_notes()

    def load_notes(self):
        try:
            with open(self.file_path, 'r') as file:
                data = file.read()
                if data:
                    self.notes = json.loads(data)
                else:
                    self.notes = []
        except FileNotFoundError:
            self.notes = []

    def save_notes(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.notes, file, ensure_ascii=False, indent=4)

    def add_note(self, title, text):
        try:
            note_id = len(self.notes) + 1
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            note = {
                'id': note_id,
                'title': title,
                'text': text,
                'timestamp': timestamp
            }

            self.notes.append(note)
            self.save_notes()

            print('Заметка успешно добавлена! 📝')
        except Exception as e:
            print(f'Ошибка при добавлении заметки: {str(e)}')

    def read_note(self, note_id):
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    note = json.loads(line)
                    if note['id'] == note_id:
                        print('Заметка найдена! 📄')
                        print('ID:', note['id'])
                        print('Заголовок:', note['title'])
                        print('Текст:', note['text'])
                        print('Создана:', note['timestamp'])
                        return

                print('Заметка с указанным ID не найдена. 😔')

        except IOError as e:
            print('Ошибка при чтении заметки:', str(e))

    def edit_note(self, note_id, new_title, new_text):
        try:
            with open(self.file_path, 'r+') as file:
                notes = []
                for line in file:
                    note = json.loads(line)
                    if note['id'] == note_id:
                        note['title'] = new_title
                        note['text'] = new_text
                        note['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    notes.append(note)

                file.seek(0)
                file.truncate(0)
                for note in notes:
                    json.dump(note, file, ensure_ascii=False, indent=4)
                    file.write('\n')

                print('Заметка отредактирована успешно! ✏️')

        except IOError as e:
            print('Ошибка при редактировании заметки:', str(e))

    def delete_note(self, note_id):
        try:
            with open(self.file_path, 'r+') as file:
                notes = []
                for line in file:
                    note = json.loads(line)
                    if note['id'] != note_id:
                        notes.append(note)

                file.seek(0)
                file.truncate(0)
                for note in notes:
                    json.dump(note, file, ensure_ascii=False, indent=4)
                    file.write('\n')

                print('Заметка удалена успешно! 🗑️')

        except IOError as e:
            print('Ошибка при удалении заметки:', str(e))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Управление заметками')
    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')

    add_parser = subparsers.add_parser('add', help='Добавить новую заметку')
    add_parser.add_argument('title', type=str, help='Заголовок заметки')
    add_parser.add_argument('text', type=str, help='Текст заметки')

    read_parser = subparsers.add_parser('read', help='Прочитать заметку')
    read_parser.add_argument('note_id', type=str, help='ID заметки')

    edit_parser = subparsers.add_parser('edit', help='Отредактировать заметку')
    edit_parser.add_argument('note_id', type=str, help='ID заметки')
    edit_parser.add_argument('new_title', type=str, help='Новый заголовок заметки')
    edit_parser.add_argument('new_text', type=str, help='Новый текст заметки')

    delete_parser = subparsers.add_parser('delete', help='Удалить заметку')
    delete_parser.add_argument('note_id', type=str, help='ID заметки')

    args = parser.parse_args()

    note_manager = NoteManager('notes.json')

    if args.command == 'add':
        note_manager.add_note(args.title, args.text)
    elif args.command == 'read':
        note_manager.read_note(args.note_id)
    elif args.command == 'edit':
        note_manager.edit_note(args.note_id, args.new_title, args.new_text)
    elif args.command == 'delete':
        note_manager.delete_note(args.note_id)
