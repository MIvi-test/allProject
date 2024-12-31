from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton,KeyboardButton



class Keyboards:
    @staticmethod
    def skip_photo() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Создать резюме", callback_data="create_resume"),
                    InlineKeyboardButton(text="Просмотреть резюме", callback_data="view_resumes")
                ],
                [
                    InlineKeyboardButton(text="Скачать резюме", callback_data="download_resume"),
                    InlineKeyboardButton(text="Редактировать резюме", callback_data="edit_resume")
                ],
                [
                    InlineKeyboardButton(text="Удалить резюме", callback_data="delete_resume")
                ]
            ],
            resize_keyboard=True
        )
    
    @staticmethod
    def main_menu() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="/start"),
                    KeyboardButton(text="/оценка")
                ],
                [
                    KeyboardButton(text="/добавить"),
                    KeyboardButton(text="/Редактировать")
                ],
                [
                    KeyboardButton(text="Удалить из коллекции"),
                    KeyboardButton(text="/стоп")
                ]
            ],
            resize_keyboard=True
        )