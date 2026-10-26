# Monitor de cita previa · Registro Civil de Elda

Bot que vigila la disponibilidad de citas en el Registro Civil de Elda (Generalitat Valenciana) y avisa por **Telegram** en cuanto aparece un hueco libre, con el enlace directo para reservar.

Conseguir cita en algunos registros civiles puede llevar semanas de entrar a la web a mano varias veces al día. Este bot hace esa comprobación cada 5 minutos, de forma automática y gratuita, sin necesidad de tener un ordenador encendido.

## Cómo funciona

```
GitHub Actions (cada 5 min)
        │
        ▼
check_once.py ──► API pública de cita previa (calendario del centro y servicio)
        │
        ├── ¿Hay días con estado disponible?
        │        │
        │        ├── Sí ──► Telegram: "Hay cita disponible" + días + enlace de reserva
        │        └── No ──► Telegram: "Sigo vigilando"
        ▼
   Fin de la ejecución (el cron de Actions hace de bucle)
```

1. Un workflow de **GitHub Actions** se ejecuta con un `cron` cada 5 minutos.
2. `check_once.py` consulta el endpoint JSON del calendario de cita previa para el centro y el servicio configurados.
3. Filtra los días cuyo estado indica disponibilidad.
4. Envía el resultado por la **API de bots de Telegram**, con el enlace de reserva listo para pulsar desde el móvil.

## Tecnologías

- **Python 3** con la librería estándar (`urllib`, `json`), sin dependencias externas.
- **GitHub Actions** como planificador: no necesita servidor propio y no tiene coste.
- **API de bots de Telegram** para las notificaciones.
- **GitHub Secrets** para el token del bot y el chat ID: no hay credenciales en el código.

## Puesta en marcha

1. Crea un bot con [@BotFather](https://t.me/BotFather) y guarda su token.
2. Consigue tu chat ID (por ejemplo, escribiendo a tu bot y consultando `getUpdates`).
3. Haz un fork de este repositorio.
4. En **Settings → Secrets and variables → Actions**, añade:
   - `TELEGRAM_TOKEN`
   - `TELEGRAM_CHAT_ID`
5. En la pestaña **Actions**, activa el workflow. Puedes lanzarlo a mano con **Run workflow**.

Para vigilar otro registro civil, cambia `CENTRO`, `SERVICIO` y `UUID` al principio de `check_once.py`.

## Estructura

```
.
├── check_once.py                      # Una comprobación por ejecución
└── .github/workflows/monitor.yml      # Cron cada 5 minutos
```

## Decisiones de diseño

- **Una comprobación por ejecución**: el bucle lo hace el `cron` de Actions, así el script es simple y no depende de un proceso que tenga que estar siempre vivo.
- **Sin dependencias**: arranca en segundos en el runner y no hay nada que instalar.
- **Credenciales fuera del código**: se leen de variables de entorno que GitHub inyecta desde los secrets.

---

Hecho por [Jhonatan Cruz](https://jhonatancrruzz.com) · [LinkedIn](https://www.linkedin.com/in/jhonatancrruzz/)
