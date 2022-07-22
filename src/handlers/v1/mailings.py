from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix='/mailings')


class MailingCreateModel(BaseModel):

    text: str


class MailingCreateResponseModel(MailingCreateModel):

    id: int


@router.delete('/{mailing_id}', status_code=204)
def delete_mailing_from_telegram(mailing_id: int):
    return


@router.post('/', status_code=201, response_model=MailingCreateResponseModel)
def delete_mailing_from_telegram(input_data: MailingCreateModel):
    return MailingCreateResponseModel(id=1, text=input_data.text)
