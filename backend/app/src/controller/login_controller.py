import jwt
import uuid
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict
from config.enums import  RedisInitKeyConfig
from config.env import AppConfig, JwtConfig
from config.get_db import get_db
from src.entity.vo.login_vo import UserLogin, UserRegister, Token
from src.service.login_service import LoginService
from utils.log_util import logger
from utils.response_util import ResponseUtil

loginController = APIRouter()


class CustomOAuth2PasswordRequestForm(OAuth2PasswordRequestForm):
    """
    自定义OAuth2PasswordRequestForm类，增加验证码及会话编号参数
    """

    def __init__(
            self,
            grant_type: str = Form(default=None, regex='password'),
            username: str = Form(),
            password: str = Form(),
            scope: str = Form(default=''),
            client_id: Optional[str] = Form(default=None),
            client_secret: Optional[str] = Form(default=None),
            code: Optional[str] = Form(default=''),
            uuid: Optional[str] = Form(default=''),
            login_info: Optional[Dict[str, str]] = Form(default=None),
    ):
        super().__init__(
            grant_type=grant_type,
            username=username,
            password=password,
            scope=scope,
            client_id=client_id,
            client_secret=client_secret,
        )
        self.code = code
        self.uuid = uuid
        self.login_info = login_info


@loginController.post('/login', response_model=Token)
async def login(
        request: Request, form_data: CustomOAuth2PasswordRequestForm = Depends(),
        query_db: AsyncSession = Depends(get_db)
):
    captcha_enabled = (
        True
        if await request.app.state.redis.get(f'{RedisInitKeyConfig.SYS_CONFIG.key}:sys.account.captchaEnabled')
           == 'true'
        else False
    )
    user = UserLogin(
        userName=form_data.username,
        password=form_data.password,
        code=form_data.code,
        uuid=form_data.uuid,
        loginInfo=form_data.login_info,
        captchaEnabled=captcha_enabled,
    )
    result = await LoginService.authenticate_user(request, query_db, user)
    access_token_expires = timedelta(minutes=JwtConfig.jwt_expire_minutes)
    session_id = str(uuid.uuid4())
    access_token = await LoginService.create_access_token(
        data={
            'user_id': str(result[0].user_id),
            'user_name': result[0].user_name,
            'dept_name': result[1].dept_name if result[1] else None,
            'session_id': session_id,
            'login_info': user.login_info,
        },
        expires_delta=access_token_expires,
    )
    if AppConfig.app_same_time_login:
        await request.app.state.redis.set(
            f'{RedisInitKeyConfig.ACCESS_TOKEN.key}:{session_id}',
            access_token,
            ex=timedelta(minutes=JwtConfig.jwt_redis_expire_minutes),
        )
    else:
        # 此方法可实现同一账号同一时间只能登录一次
        await request.app.state.redis.set(
            f'{RedisInitKeyConfig.ACCESS_TOKEN.key}:{result[0].user_id}',
            access_token,
            ex=timedelta(minutes=JwtConfig.jwt_redis_expire_minutes),
        )
    await UserService.edit_user_services(
        query_db, EditUserModel(userId=result[0].user_id, loginDate=datetime.now(), type='status')
    )
    logger.info('登录成功')
    # 判断请求是否来自于api文档，如果是返回指定格式的结果，用于修复api文档认证成功后token显示undefined的bug
    request_from_swagger = request.headers.get('referer').endswith('docs') if request.headers.get('referer') else False
    request_from_redoc = request.headers.get('referer').endswith('redoc') if request.headers.get('referer') else False
    if request_from_swagger or request_from_redoc:
        return {'access_token': access_token, 'token_type': 'Bearer'}
    return ResponseUtil.success(msg='登录成功', dict_content={'token': access_token})


@loginController.post('/register', response_model=CrudResponseModel)
async def register_user(request: Request, user_register: UserRegister, query_db: AsyncSession = Depends(get_db)):
    user_register_result = await LoginService.register_user_services(request, query_db, user_register)
    logger.info(user_register_result.message)

    return ResponseUtil.success(data=user_register_result, msg=user_register_result.message)
