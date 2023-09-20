import asyncio
import json
import re
import subprocess
from dataclasses import dataclass


@dataclass
class UserTraffic:
    uplink: str = ""
    downlink: str = ""


class _XRAYService:
    def __init__(self):
        self._rc: int | None = 0
        self._stdout = ""
        self._stderr = ""

    async def restart(self):
        await self._run_command("systemctl restart xray.service")

    async def get_user_traffic(self, username: str) -> UserTraffic:
        rc, stdout, stderr = await self._run_command(
            f"xray api statsquery --server=127.0.0.1:10085 -pattern '{username}' | jq .stat"
        )
        raw_data = json.loads(stdout or "[]")
        traffic = UserTraffic()
        for part in raw_data:
            if part["name"].endswith("uplink"):
                traffic.uplink = part["value"]
            if part["name"].endswith("downlink"):
                traffic.downlink = part["value"]
        return traffic

    async def check_status(self):
        self._rc, self._stdout, self._stderr = await self._run_command(
            "systemctl status xray.service"
        )

    def is_running(self) -> bool:
        return "active (running)" in self._stdout

    def get_memory(self) -> str:
        memory = re.search(r"Memory: (\S+)", self._stdout)
        if memory:
            return memory.group(0)
        return "-"

    @staticmethod
    async def _run_command(command: str) -> tuple[int | None, str, str]:
        # Создаем подпроцесс для выполнения команды
        process = await asyncio.create_subprocess_shell(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        # Ждем завершения подпроцесса и получаем результат
        stdout, stderr = await process.communicate()
        # Возвращаем код выхода, стандартный вывод и стандартный вывод ошибок
        return (
            process.returncode,
            stdout.decode(errors="ignore"),
            stderr.decode(errors="ignore"),
        )


xray_service = _XRAYService()
