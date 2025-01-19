from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton,KeyboardButton



class Keyboards:
    @staticmethod
    def skip_photo() -> ReplyKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="вернуться", callback_data='back')
                ]
            ],
            resize_keyboard=True
        )
    
    @staticmethod
    def main_menu() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    
                    KeyboardButton(text="/оценка"),
                    KeyboardButton(text="/стоп")
                    # KeyboardButton(text="/Редактировать")
                ],
                [
                    KeyboardButton(text="/отложенное"),
                    KeyboardButton(text="/добавить")
                ]
            ],
            resize_keyboard=True
        )
    @staticmethod
    def inline_skip() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="СКИП!", callback_data='skip'),
                    InlineKeyboardButton(text="повтор", callback_data='repeat')
                ]
            ]
        )
    