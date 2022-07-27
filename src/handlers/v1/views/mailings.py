from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from services.mailing import Mailing

router = APIRouter(prefix='/mailings')


class MailingModel(BaseModel):
    """Модель рассылки."""

    id: int


class MailingCreateModel(BaseModel):
    """Модель для создания рассылок."""

    text: str


class MailingCreateResponseModel(MailingCreateModel):
    """Модель ответа запроса создания рассылок."""

    id: int


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[MailingModel])
def get_mailings():
    """Получить список рассылок.

    :return: list[MailingModel]
    """
    return [MailingModel(id=1)]


@router.delete('/{mailing_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_mailing_from_telegram(mailing_id: int):
    """Удаление сообщений, входящих в рассылку.

    :param mailing_id: int
    """
    return  # noqa: WPS324


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=MailingCreateResponseModel)
async def create_mailing_from_telegram(
    input_data: MailingCreateModel,
    mailing_service: Mailing = Depends(),
) -> MailingCreateResponseModel:
    """Создание рассылки.

    :param input_data: MailingCreateModel
    :param mailing_service: Mailing
    :return: MailingCreateResponseModel
    """
    await mailing_service.create(input_data.text)
    return MailingCreateResponseModel(id=1, text=input_data.text)
