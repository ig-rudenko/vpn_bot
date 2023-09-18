from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from magic_filter import F

from ..service.account import Profile
from ..service.exc import ProfileAlreadyExist
from ..states.account import RegisterState

router = Router()


@router.message(Command("reg"))
@router.callback_query(F.data == "register")
async def start_register(callback: types.CallbackQuery, state: FSMContext):
    if await Profile.exist(callback.from_user.id):
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

    elif not await Profile.username_is_available(username):
        await message.answer("Такой username уже занят, выберите другой")

    else:
        await state.update_data(username=username)
        await message.answer("Теперь введите пароль")
        await state.set_state(RegisterState.password)


@router.message(RegisterState.password)
async def set_password(message: types.Message, state: FSMContext):
    password = message.text.lower()
    if len(password) > 128:
        await message.answer("Пароль не должен превышать 128 символов")
    else:
        await state.update_data(password=password)
        user_data = await state.get_data()
        print(user_data)
        profile = Profile(tg_user=message.from_user)
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
