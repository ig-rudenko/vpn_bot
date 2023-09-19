import asyncio
import subprocess


class _XRAYService:
    async def reload(self):
        await self._run_command("systemctl reload xray")

    async def is_running(self) -> bool:
        rc, stdout, stderr = await self._run_command("systemctl status xray")
        return "active (running)" in stdout

    @staticmethod
    async def _run_command(command: str) -> tuple[int | None, str, str]:
        # Создаем подпроцесс для выполнения команды
        process = await asyncio.create_subprocess_shell(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        # Ждем завершения подпроцесса и получаем результат
        stdout, stderr = await process.communicate()
        # Возвращаем код выхода, стандартный вывод и стандартный вывод ошибок
        return process.returncode, stdout.decode(), stderr.decode()


xray_service = _XRAYService()
