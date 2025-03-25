from fastapi import HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from config.get_db import get_db
from src.entity.vo.user_vo import CurrentUserModel


class LoginService:

    async def get_current_user(
            request: Request,
            query_db: AsyncSession = Depends(get_db),
    ) -> CurrentUserModel:
        """
        获取当前用户信息
        :param request:
        :param query_db:
        :return:
        """
        token = request.headers.get('Authorization')
        if not token:
            raise HTTPException(status_code=404, detail='未登录')
        token = token.split(' ')[1]
