from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter(prefix='/mailings')


class MailingCreateModel(BaseModel):
    """Модель для создания рассылок."""

    text: str


class MailingCreateResponseModel(MailingCreateModel):
    """Модель ответа запроса создания рассылок."""

    id: int


@router.delete('/{mailing_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_mailing_from_telegram(mailing_id: int):
    """Удаление сообщений, входящих в рассылку.

    :param mailing_id: int
    """
    return  # noqa: WPS324


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=MailingCreateResponseModel)
def create_mailing_from_telegram(input_data: MailingCreateModel) -> MailingCreateResponseModel:
    """Создание рассылки.

    :param input_data: MailingCreateModel
    :return: MailingCreateResponseModel
    """
    return MailingCreateResponseModel(id=1, text=input_data.text)
