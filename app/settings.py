import os
from fastapi import status

class Settings:
    class database:
        URL: str = os.environ.get('DATABASE_URL')

    class error:
        E001: tuple = (status.HTTP_400_BAD_REQUEST, 'Invalid file.')
        E002: tuple = (status.HTTP_400_BAD_REQUEST, 'File data isn`t valid.')
        E003: tuple = (status.HTTP_500_INTERNAL_SERVER_ERROR, 'It was not possible to generate bill.')
        E004: tuple = (status.HTTP_500_INTERNAL_SERVER_ERROR, 'It was not possible to send the email.')
        E005: tuple = (status.HTTP_500_INTERNAL_SERVER_ERROR, 'It was not possible to store bills in database.')

    class error_codes:
        INVALID_FILE: str = 'E001'
        FILE_VALIDATION: str = 'E002'
        BILL_GENERATION: str = 'E003'
        SEND_EMAIL: str = 'E004'
        STORE_BILLS: str = 'E005'

    class email:
        SUBJECT: str = 'Boleto para pagamento.'
        PORT: int = 465
        SENDER_EMAIL: str = 'email@mail.com'

settings = Settings()