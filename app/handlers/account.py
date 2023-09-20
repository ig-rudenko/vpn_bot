from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram import F

from ..service.account import ProfileService
from ..service.exc import ProfileAlreadyExist, ProfileDataInvalid
from ..states.account import RegisterState, LoginState

router = Router()


@router.callback_query(F.data == "register")
async def start_register(callback: types.CallbackQuery, state: FSMContext):
    if await ProfileService.exist(callback.from_user.id):
        await callback.message.answer("Вы уже зарегистрированы")
    else:
        await callback.message.answer("Введите ваш username")
        await state.set_state(RegisterState.username)
    await callback.answer()


@router.message(RegisterState.username)
async def set_username(message: types.Message, state: FSMContext):
    username = message.text.lower()
    if len(username) > 128:
        await message.answer("Имя пользователя не должно превышать 128 символов")

    elif not await ProfileService.username_is_available(username):
        await message.answer("Такой username уже занят, выберите другой")

    else:
        await state.update_data(username=username)
        await message.answer("Теперь введите пароль")
        await state.set_state(RegisterState.password)


@router.message(RegisterState.password)
async def set_password(message: types.Message, state: FSMContext):
    password = message.text
    if len(password) > 128:
        await message.answer("Пароль не должен превышать 128 символов")
    else:
        await state.update_data(password=password)
        user_data = await state.get_data()
        profile = ProfileService(tg_id=message.from_user.id)
        try:
            await profile.create(
                username=user_data["username"],
                password=user_data["password"],
            )
        except ProfileAlreadyExist as exc:
            await message.answer(exc.message)
            await message.answer("Укажите username заново")
            await state.set_state(RegisterState.username)
        else:
            await message.answer("Вы были успешно зарегистрированы")

        await state.clear()


# ================ LOGIN ==================


@router.callback_query(F.data == "login")
async def start_register(callback: types.CallbackQuery, state: FSMContext):
    if await ProfileService.exist(callback.from_user.id):
        await callback.message.answer("Вы уже вошли")
    else:
        await callback.message.answer("Введите ваш username")
        await state.set_state(LoginState.username)
    await callback.answer()


@router.message(LoginState.username)
async def set_username(message: types.Message, state: FSMContext):
    username = message.text.lower()
    if len(username) > 128:
        await message.answer("Имя пользователя не должно превышать 128 символов")

    elif await ProfileService.username_is_available(username):
        await message.answer("Такой username не существует")

    else:
        await state.update_data(username=username)
        await message.answer("Теперь введите пароль")
        await state.set_state(LoginState.password)


@router.message(LoginState.password)
async def set_password(message: types.Message, state: FSMContext):
    password = message.text
    user_data = await state.get_data()
    try:
        profile = await ProfileService.get(
            username=user_data["username"],
            password=password,
        )
        await ProfileService.set_profile_to_tg_user(profile, message.from_user.id)
    except ProfileDataInvalid as exc:
        await message.answer(f"{exc.message}\nУкажите заново")
        await state.set_state(LoginState.password)
        return
    else:
        await message.answer("Вы успешно вошли в учетную запись")

    await state.clear()
