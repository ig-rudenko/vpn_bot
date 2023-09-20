## Запуск

Необходимо создать сервис со следующим содержимым:

```ini
[Unit]
Description=Telegram bot for VPN
After=syslog.target
After=network.target

[Service]
Environment="TG_TOKEN={token}"
Environment="XRAY_SERVER_IP={ip}"
Environment="XRAY_PUBLIC_KEY={key}"
Environment="XRAY_SHORT_ID={sid}"
Environment="XRAY_CONFIG_PATH={path_to_xray_config.json}"

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