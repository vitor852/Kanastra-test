from pydantic import ValidationError
from sqlalchemy.orm import Session
from fastapi import UploadFile
from sqlalchemy import select
from datetime import date
import logging
import codecs
import csv

from .schemas.debt import Debt as DebtSchema
from .models import Debt
from .settings import settings
from .utils import timed


logger = logging.getLogger(__name__)


class Data:
    def __init__(self, db: Session):
        self.db = db
        self.file = None
        self.debt_drafts = []
        self.bills = []

    def from_file(self, file_: UploadFile):
        self.file = file_.file
        self.__read_and_validate_data()
        return self

    @timed
    def process(self):
        self.__filter_already_processed()
        logger.info('Processing pending debts.')
        list(map(self.__pipeline, self.debt_drafts))
        self.__store_bills()

    @timed
    def __read_and_validate_data(self):
        logger.info('Reading and validating file content.')

        decoded_content = codecs.iterdecode(self.file, 'utf-8')
        csv_file = csv.DictReader(decoded_content)

        logger.info('Reading complete')

        try:
            debt_drafts = [DebtSchema(**item) for item in csv_file]

            sorted_debt_drafts = sorted(debt_drafts, key=lambda draft: draft.debtDueDate)

            logger.info('Validation complete')
            logger.info(f'{len(debt_drafts)} items found.')

            self.debt_drafts = sorted_debt_drafts
        except ValidationError as e:
            logger.error('Validation failed.')
            logger.info(e.errors())

            raise Exception(settings.error_codes.FILE_VALIDATION, e.errors())
        
    @timed
    def __query_processed_intersection(self, ids):
        logger.info('Querying bills history.')
        return self.db.scalars(
            select(Debt.reference_id)
            .where(Debt.reference_id.in_(ids))
            ).all()
        
    @timed
    def __filter_already_processed(self):
        logger.info('Verifying if some debt is processed.')


        draft_ids = [draft.debtId for draft in self.debt_drafts]
        already_processed_draft_ids = self.__query_processed_intersection(draft_ids)
        processed_debts_qtd = len(already_processed_draft_ids)


        if processed_debts_qtd > 0 and processed_debts_qtd != len(draft_ids):
            last_processed_debt_id = already_processed_draft_ids[-1]
            last_processed_debt_id_index = draft_ids.index(last_processed_debt_id)
            not_processed_debts_index_begin = last_processed_debt_id_index + 1

            logger.info(
                '{} processed debts found, {} left.'.format(
                    len(self.debt_drafts[:last_processed_debt_id_index]),
                    len(self.debt_drafts[not_processed_debts_index_begin:])
                )
            )

            self.debt_drafts = self.debt_drafts[not_processed_debts_index_begin:]
            return

        logger.info(f'Processed debts not found, {len(self.debt_drafts)} to be processed.')
        return

    @timed
    def __store_bills(self):
        try:
            self.db.execute(Debt.__table__.insert(), self.bills)
            self.db.commit()
        except:
            raise Exception(settings.error_codes.STORE_BILLS, None)

    def __pipeline(self, draft: DebtSchema):
        def generate_bill(draft: DebtSchema):
            logger.debug(f'Generating bill for debt with id: {draft.debtId}')

            try:
                bill_url = Bill(
                    name=draft.name,
                    amount=draft.debtAmount,
                    due_date=draft.debtDueDate
                ).generate()

                logger.debug(f'Successfully generated bill.')
                logger.debug(f'Bill url: {bill_url}')

                return bill_url
            except Exception as e:
                logger.error(f'Error generating bill for debt with id: {draft.debtId}')
                logger.info(e.args[0])
                raise Exception(settings.error_codes.BILL_GENERATION, e.args[0])
    
        def send_bill_email(email: str, bill_url: str):
            logger.debug(f'Sending generated bill to email: {email}')

            try:
                Email(receiver_email=email, attachment=bill_url).send()
                logger.debug('Successfully sended bill.')
            except Exception as e:
                logger.debug(f'Error sending to email: {email}')
                logger.debug(e.args[0])

                raise Exception(settings.error_codes.SEND_EMAIL, e.args[0])

        bill_url = generate_bill(draft)
        send_bill_email(draft.email, bill_url)

        logger.debug(f'Debt pipeline finished, bill id: {draft.debtId}')
        
        self.bills.append(
            dict(
                bill_url=bill_url,
                reference_id = draft.debtId
            )
        )


class Email:
    def __init__(self, receiver_email: str, attachment: dict):
        self.receiver_email = receiver_email
        self.attachment = attachment
        self.subject = settings.email.SUBJECT
        self.port = settings.email.PORT
        self.sender_email = settings.email.SENDER_EMAIL

    def send(self):
        return None
        
    

class Bill:
    def __init__(self, due_date: date, name: str, amount: float):
        self.due_date = due_date
        self.name = name
        self.amount = amount

    def generate(self):
        return 'https://valid.file.url'