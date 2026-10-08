# Evidencias de integración continua

Verificación realizada el **7 de octubre de 2026**, hora de Guatemala.
Los registros de GitHub usan UTC; por eso sus marcas de tiempo indican
8 de octubre. Son ejecuciones reales, no ejemplos simulados.

## Repositorio y pruebas

- Repositorio público: https://github.com/gabrielpaz2003/AdminSP7
- Código inicial conservado desde `Its-Japo/AdminSP7`.
- Python 3.13 y pytest 8.3.3: **77 pruebas aprobadas**.
- Comprobación de errores intencionales: **5 de 5 mutaciones detectadas**.
- [Salida de las pruebas locales y mutaciones](evidence/pruebas-locales.txt).

## PR #1: fallo, bloqueo, corrección e integración

[Abrir el Pull Request de demostración](https://github.com/gabrielpaz2003/AdminSP7/pull/1).

| Paso | Evidencia | Resultado |
| --- | --- | --- |
| Error deliberado en `square` | Commit [`f4d6d02`](https://github.com/gabrielpaz2003/AdminSP7/commit/f4d6d02843ac54bb9879923ca3eac906de0cd1eb) | Retorna `n + n`; `square(4)` entrega 8 en vez de 16. |
| CI fallido por `pull_request` | [Ejecución 37715046914](https://github.com/gabrielpaz2003/AdminSP7/actions/runs/37715046914) | **3 fallidas, 74 aprobadas**. |
| Protección aplicada | [Estado del PR](evidence/pr-fallo.json) y [rechazo del merge](evidence/merge-bloqueado.txt) | `mergeStateStatus: BLOCKED`; GitHub rechaza el merge por la política de la rama. |
| Corrección en el mismo PR | Commit [`9fea395`](https://github.com/gabrielpaz2003/AdminSP7/commit/9fea395076700ec4ca7765fe53a8c81908bb5c51) | Restablece `n * n`. |
| CI aprobado por `pull_request` | [Ejecución 37715183691](https://github.com/gabrielpaz2003/AdminSP7/actions/runs/37715183691) | **77 aprobadas**. |
| Merge habilitado | [Estado corregido](evidence/pr-corregido.json) | `mergeStateStatus: CLEAN`, check obligatorio `SUCCESS`. |
| Integración realizada | [Registro del PR integrado](evidence/pr-integrado.json) | Estado `MERGED`; commit `35d5d8d1ed044a6bdb913cac19a323bcfb461b26`. |

El merge se realizó sin bypass de administrador y después de obtener el check
correcto. La rama `main` contiene la implementación funcional y el historial
conserva el commit defectuoso y su corrección.

Los logs del CI también están guardados en el repositorio:
[fallo](evidence/run-fallo.log) y [éxito](evidence/run-exito.log). Los enlaces a
Actions son la evidencia remota; las copias ayudan cuando expire su retención.

## Regla de protección verificada

La [respuesta de la API](evidence/proteccion-main.json) confirma:

- Check obligatorio: `Pruebas unitarias`, emitido por GitHub Actions
  (App ID `15368`).
- `strict: true`: la rama debe estar actualizada antes del merge.
- `enforce_admins.enabled: true`: la protección incluye a los administradores.
- Pull Request obligatorio, con cero aprobaciones adicionales requeridas.
- Force pushes y eliminación de `main` deshabilitados.

El YAML ejecuta la prueba y la protección exige su resultado. Ambas partes son
necesarias para cumplir el criterio de bloqueo del merge.

## Repetir en clase

Usar la [guía de demostración](DEMOSTRACION.md) y una nueva rama. El PR #1 ya
integrado conserva la evidencia previa; para la presentación en vivo hay que
mostrar un nuevo PR pasando nuevamente de rojo a verde.
