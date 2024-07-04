from pydantic import BaseModel, model_serializer
from datetime import date

class Debt(BaseModel):
    debtId: str

    name: str
    governmentId: str
    email: str

    debtAmount: float
    
    debtDueDate: date

    @model_serializer
    def to_dict(self):
        return dict(
            id=self.debtId,
            name=self.name,
            government_id=self.governmentId,
            email=self.email,
            amount=self.debtAmount,
            due_date=self.debtDueDate,
        )