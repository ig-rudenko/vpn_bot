## Запуск

Создаем файл `/etc/sysconfig/tg_bot`:

```ini
TG_TOKEN={token}
XRAY_SERVER_IP={ip}
XRAY_PUBLIC_KEY={key}
XRAY_SHORT_ID={sid}
XRAY_CONFIG_PATH={path_to_xray_config.json}
BECOME_TOKEN={superuser_token}
```

Необходимо создать сервис со следующим содержимым:

```ini
[Unit]
Description=Telegram bot for VPN
After=syslog.target
After=network.target

[Service]
EnvironmentFile=/etc/sysconfig/tg_bot

Type=simple
WorkingDirectory={path_to_vpn_bot}

User=root
Group=root

ExecStart={path_to_vpn_bot}/venv/bin/python bot.py

TimeoutSec=10
Restart=always

[Install]
WantedBy=multi-user.target
```