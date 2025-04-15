from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.schemas.user_schemas import UserCreate, UserOut, Token
from app.core.security import verify_password, create_access_token
from app.db.session import get_db
from app.cruds.user_crud import UserCRUD

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")
router = APIRouter()
@router.post("/sign-up/", response_model=UserOut, summary = "Регистрация")
async def sign_up(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Проверяет, не зарегистрирован ли уже пользователь с таким email.
    Если нет — создает.
    """
    existing_user = await UserCRUD.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует"
        )

    # Создаем нового пользователя
    new_user = await UserCRUD.create_user(db, user_data.email, user_data.password)
    return UserOut.from_orm(new_user)

@router.post("/login/", response_model=Token, summary = "Ввод пароля")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), # Принимаем форму логина (username, password)
    db: AsyncSession = Depends(get_db)                # Подключаемся к базе данных
):
    """
    Проверяет существование пользователя, сравнивает пароль, возвращает JWT-токен.
    """
    user = await UserCRUD.get_user_by_email(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Неверный email или пароль")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный email или пароль")

    access_token = create_access_token({"sub": user.email})
    return Token(access_token=access_token)

# Импортируем дополнительные зависимости и модели (внизу файла, чтобы избежать циклических импортов)
from app.api.deps import get_current_user
from app.models.user import User

@router.get("/users/me/", response_model=UserOut, summary = "Инфо о пользователе")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Возвращает информацию о текущем (авторизованном) пользователе.
    """
    return current_user
