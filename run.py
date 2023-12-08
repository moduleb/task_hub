
import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.config import config
from app.logger import log
from app.routers import users, login, register, logout

# создание приложения
app = FastAPI()

# перенаправление на /docs при обращении на "/"
@app.get("/", response_class=RedirectResponse,
         include_in_schema=False)
def redirect():
    return "/docs"


# регистрация эндпоинтов
app.include_router(users.router, prefix='/users', tags=["Users"])
app.include_router(register.router, prefix='/users', tags=["Authentication"])
app.include_router(login.router, prefix='/users', tags=["Authentication"])
app.include_router(logout.router, prefix='/users', tags=["Authentication"])

# запуск приложения
if __name__ == "__main__":
    log.info(f'Загружена конфигурация {config.config_type}')
    uvicorn.run(app, host='0.0.0.0')