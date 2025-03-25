from pydantic import BaseModel, EmailStr, Field, ConfigDict
from pydantic.alias_generators import to_camel


class UserLogin(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    phone: str = Field(description='手机号')
    email: str = Field(description='邮箱')
    name: str = Field(description='用户名')


class Token(BaseModel):
    access_token: str = Field(description='token信息')
    token_type: str = Field(description='token类型')


class UserRegister(BaseModel):
    pass
