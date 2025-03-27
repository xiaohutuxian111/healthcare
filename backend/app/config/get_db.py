from backend.app.config.database import AsyncSessionLocal, async_engine, Base
from backend.app.utils.log_util import logger


async def get_db():
    """
    每一个请求处理完毕后会关闭当前连接，不同的请求使用不同的连接

    :return:
    """
    async with AsyncSessionLocal() as current_db:
        yield current_db


async def init_create_table():
    """
    应用启动时初始化数据库连接

    :return:
    """
    logger.info('初始化数据库连接...')
    async with async_engine.begin() as conn:
        logger.info(f"连接信息:{conn}")
        logger.info(f"准备创建的表: {Base.metadata.tables.keys()}")
        await conn.run_sync(Base.metadata.create_all)
    logger.info('数据库连接成功')


if __name__ == '__main__':
    import asyncio
    asyncio.run(init_create_table())
