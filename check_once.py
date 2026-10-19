"""
Monitor de cita previa - Registro Civil Elda (GVA) - version para GitHub Actions.
Una sola comprobacion por ejecucion (el cron de Actions hace de bucle).
No usa winsound ni abre navegador (no hay pantalla en el runner): solo
manda Telegram. El enlace que manda es pulsable directamente desde el movil.
"""

import json
import os
import urllib.parse
import urllib.request
from datetime import datetime

CENTRO = 46
SERVICIO = 300
UUID = "01E4-33B69-2883-5B9B8"

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

CALENDAR_URL = (
    f"https://sige.gva.es/qsige.localizador/citaPrevia/disponible/"
    f"centro/{CENTRO}/servicio/{SERVICIO}/calendario"
)
BOOKING_URL = f"https://sige.gva.es/qsige/citaprevia.justicia/#/va/appointment?uuid={UUID}"


def send_telegram(text: str) -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": TELEGRAM_CHAT_ID, "text": text}).encode()
    with urllib.request.urlopen(url, data=data, timeout=10) as resp:
        resp.read()


def check_once() -> list[str]:
    req = urllib.request.Request(CALENDAR_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return [d["dia"] for d in data.get("dias", []) if d.get("estado") == 0]


def main() -> None:
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M")
    try:
        disponibles = check_once()
    except Exception as exc:
        print(f"Error consultando: {exc}")
        return

    if disponibles:
        mensaje = (
            "Hay cita disponible en Registro Civil Elda:\n"
            f"{', '.join(disponibles)}\n\n"
            f"Entra YA: {BOOKING_URL}"
        )
        send_telegram(mensaje)
        print("DISPONIBLE:", disponibles)
    else:
        send_telegram(f"Sigo vigilando, sin citas todavia ({ahora})")
        print("Sin citas todavia")


if __name__ == "__main__":
    main()
