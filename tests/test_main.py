from datetime import date
from fastapi import status
from io import BytesIO

from app.models import Debt
from app.schemas.debt import Debt as DebtSchema
from app.services import Bill, Email


def test_store_valid_debt(db):
    data = dict(
        reference_id = 'ea23f2ca-663a-4266-a742-9da4c9f455b3'
    )
    debt = Debt(**data)
    db.add(debt)
    db.commit()

def test_debt_validation():
    data = dict(
        name = 'Valid Name',
        debtId = 'ea23f2ca-663a-4266-a742-9da4c9f455b3',
        governmentId = '9558',
        email = 'valid@email.com',
        debtAmount = 7811,
        debtDueDate = '2024-01-19'
    )
    debt_draft = DebtSchema(**data)

    assert debt_draft.name == data.get('name')
    assert debt_draft.debtId == data.get('debtId')
    assert debt_draft.governmentId == data.get('governmentId')
    assert debt_draft.email == data.get('email')
    assert debt_draft.debtAmount == data.get('debtAmount')
    assert isinstance(debt_draft.debtDueDate, date)

def test_invalid_file_extension(client):
    filename = 'invalid_file.txt'
    file_content = b'ping pong'

    response = client.post('/', files={'file': (filename, file_content)})

    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_invalid_file_content(client):
    filename = 'valid_filename.csv'
    file_content = BytesIO(b'''\
name,governmentId,email,debtAmount,debtDueDate,debtId
valid name,9558,valid@email.com,7811,20241-19,ea23f2ca-663a-4266-a742-9da4c9f455b3''') # invalid date

    response = client.post('/', files={'file': (filename, file_content)})

    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_bill_generation():
    data = dict(
        name = 'Valid Name',
        debtId = 'ea23f2ca-663a-4266-a742-9da4c9f455b3',
        governmentId = '9558',
        email = 'valid@email.com',
        debtAmount = 7811,
        debtDueDate = '2024-01-19'
    )
    debt_draft = DebtSchema(**data)
    bill_url = Bill(due_date=debt_draft.debtDueDate, name=debt_draft.name, amount=debt_draft.debtAmount).generate()

    assert bill_url == 'https://valid.file.url'

def test_main_simple_insert(client):
    filename = 'valid_filename.csv'
    file_content = BytesIO(b'''\
name,governmentId,email,debtAmount,debtDueDate,debtId
Elijah Santos,9558,janet95@example.com,7811,2024-01-19,ea23f2ca-663a-4266-a742-9da4c9f455b3
Samuel Orr,5486,linmichael@example.com,5662,2023-02-25,acc1794e-b264-4fab-8bb7-3400d4c4734d
Leslie Morgan,9611,russellwolfe@example.net,6177,2022-10-17,9f5a2b0c-967e-4443-a03d-9d7cdcb22155
Joseph Rivera,1126,urangel@example.org,7409,2023-08-16,33bec852-beee-477f-ae65-1475c74e1966
Jessica James,1525,lisa11@example.net,5829,2024-01-18,e2dba21b-5520-4226-82b5-90c6bb3356c55
Charles Fields,1874,melissa18@example.net,7685,2024-05-12,f94d431b-4629-4880-b4a8-047116ec5fc5
Kelly Sanchez,7032,erindavis@example.com,5932,2024-05-08,cd3359c9-e5ce-42ef-926d-b28ec70556b3
Bryan Villarreal,4133,douglasevans@example.net,5235,2024-04-21,674388d1-ebb9-4ec3-8e7e-0776a8855dc9
Dennis Davis,7479,angela12@example.com,9269,2022-10-23,a65abc5f-4760-42a5-9dc3-a68526e48a5f
Crystal Williams,5352,annabrown@example.org,8779,2023-11-19,3f378517-33ba-4dc5-9595-28bd87ca921e
Deanna Williams,9954,rschmidt@example.net,9619,2023-11-24,04b3b8fd-fc5a-42dc-bf37-1719da45538
Jordan Davis,5168,masondavid@example.com,5081,2022-12-25,140c85f1-ac06-4389-ad9f-71c704a61d55
Charles Aguirre,1507,westjeremy@example.com,4640,2023-04-01,42f374d0-3491-498c-84c7-44038b45fab8''')

    response = client.post('/', files={'file': (filename, file_content)})

    assert response.status_code == status.HTTP_200_OK

def test_main_parcial_insert(client, db):
    filename = 'valid_filename.csv'
    file_content = BytesIO(b'''\
name,governmentId,email,debtAmount,debtDueDate,debtId
Elijah Santos,9558,janet95@example.com,7811,2024-01-19,ea23f2ca-663a-4266-a742-9da4c9f455b3
Samuel Orr,5486,linmichael@example.com,5662,2023-02-25,acc1794e-b264-4fab-8bb7-3400d4c4734d
Leslie Morgan,9611,russellwolfe@example.net,6177,2022-10-17,9f5a2b0c-967e-4443-a03d-9d7cdcb22155
Joseph Rivera,1126,urangel@example.org,7409,2023-08-16,33bec852-beee-477f-ae65-1475c74e1966
Jessica James,1525,lisa11@example.net,5829,2024-01-18,e2dba21b-5520-4226-82b5-90c6bb3356c55
Charles Fields,1874,melissa18@example.net,7685,2024-05-12,f94d431b-4629-4880-b4a8-047116ec5fc5''')

    response = client.post('/', files={'file': (filename, file_content)})
    assert response.status_code == status.HTTP_200_OK

    debts_qtd = len(db.query(Debt).all())
    assert debts_qtd == 6

    file_content = BytesIO(b'''\
name,governmentId,email,debtAmount,debtDueDate,debtId
Kelly Sanchez,7032,erindavis@example.com,5932,2024-05-08,cd3359c9-e5ce-42ef-926d-b28ec70556b3
Bryan Villarreal,4133,douglasevans@example.net,5235,2024-04-21,674388d1-ebb9-4ec3-8e7e-0776a8855dc9
Dennis Davis,7479,angela12@example.com,9269,2022-10-23,a65abc5f-4760-42a5-9dc3-a68526e48a5f
Crystal Williams,5352,annabrown@example.org,8779,2023-11-19,3f378517-33ba-4dc5-9595-28bd87ca921e
Deanna Williams,9954,rschmidt@example.net,9619,2023-11-24,04b3b8fd-fc5a-42dc-bf37-1719da45538
Jordan Davis,5168,masondavid@example.com,5081,2022-12-25,140c85f1-ac06-4389-ad9f-71c704a61d55
Charles Aguirre,1507,westjeremy@example.com,4640,2023-04-01,42f374d0-3491-498c-84c7-44038b45fab8''')
    
    response = client.post('/', files={'file': (filename, file_content)})
    assert response.status_code == status.HTTP_200_OK

    debts_qtd = len(db.query(Debt).all())
    assert debts_qtd == 13

def test_email_send():
    response = Email(attachment='https://valid.url', receiver_email='valid@email.com').send()
    assert response == None