"""Обработчики HTTP запросов для работы с рассылками.

Classes:
    MailingModel
    MailingCreateModel
    MailingCreateResponseModel

Functions:
    get_mailings
    delete_mailing_from_telegram
    create_mailing_from_telegram
"""
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from integrations.queue_integration import NatsIntegration, QueueIntegrationInterface
from repositories.auth import UserSchema
from services.auth import User
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
def get_mailings(user: UserSchema = Depends(User.get_from_token)):
    """Получить список рассылок.

    :param user: UserSchema
    :return: list[MailingModel]
    """
    return [MailingModel(id=1)]


@router.delete('/{mailing_id}', status_code=status.HTTP_201_CREATED)
async def delete_mailing_from_telegram(
    mailing_id: int,
    user: UserSchema = Depends(User.get_from_token),
    nats_integration: QueueIntegrationInterface = Depends(NatsIntegration),
):
    """Удаление сообщений, входящих в рассылку.

    :param user: UserSchema
    :param mailing_id: int
    :param nats_integration: QueueIntegrationInterface
    """
    await nats_integration.send(
        {'mailing_id': mailing_id},
        'Mailing.Deleted',
        1,
    )


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=MailingCreateResponseModel)
async def create_mailing_from_telegram(
    input_data: MailingCreateModel,
    mailing_service: Mailing = Depends(),
    user: UserSchema = Depends(User.get_from_token),
) -> MailingCreateResponseModel:
    """Создание рассылки.

    :param input_data: MailingCreateModel
    :param mailing_service: Mailing
    :param user: UserSchema
    :return: MailingCreateResponseModel
    """
    await mailing_service.create(input_data.text)
    return MailingCreateResponseModel(id=1, text=input_data.text)
