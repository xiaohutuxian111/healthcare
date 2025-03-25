from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse

import router_manager
from config.env import AppConfig
from config.get_db import init_create_table
from config.get_redis import RedisUtil
from exceptions.handle import handle_exception
from middlewares.handle import handle_middleware
from sub_applications.handle import handle_sub_applications
# from router import router_manager

# from sub_applications.handle import handle_sub_applications
from utils.common_util import worship
from utils.log_util import logger
from fastapi import FastAPI, Request

from utils.response_util import ResponseUtil


# 生命周期事件
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f'{AppConfig.app_name}开始启动')
    worship()
    await init_create_table()
    app.state.redis = await RedisUtil.create_redis_pool()
    logger.info(f'{AppConfig.app_name}启动成功')
    yield
    await RedisUtil.close_redis_pool(app)


# 初始化FastAPI对象
app = FastAPI(
    title=AppConfig.app_name,
    description=f'{AppConfig.app_name}接口文档',
    version=AppConfig.app_version,
    lifespan=lifespan,
    root_path=AppConfig.app_root_path,
)


# 定义中间件
@app.middleware("http")
async def block_post_requests(request: Request, call_next):
    # 继续处理其他请求
    response = await call_next(request)
    return response


# 加载中间件处理方法
handle_middleware(app)
# 加载全局异常处理方法
handle_exception(app)

# # 加载路由列表
app.include_router(router_manager.register_router())
# # 挂载子应用
handle_sub_applications(app)
