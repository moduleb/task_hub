"""
Создание приложения, регистрация endpoints,
Переадресация для главной страницы
Запуск приложения
"""

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.config import config
from app.logger import log
from app.routers import tasks

# Создание приложения
app = FastAPI(title="Task Hub")
log.debug('App created: %s', app)

# Регистрация эндпоинтов
app.include_router(tasks.router, prefix='/tasks', tags=["Tasks"])
log.debug('Router registered: /tasks')


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirect to /openapi.json when accessing "/" endpoint"""
    return RedirectResponse(url="/docs")


# Запуск приложения
if __name__ == "__main__":
    log.info('Configuration loaded: %s', config.config_type)
    uvicorn.run(app, host='0.0.0.0')
