# Demostración en vivo: lunes 19 de octubre de 2026

Duración sugerida: 5 a 7 minutos. Una persona explica la librería y las pruebas;
la otra explica el workflow, la protección y el Pull Request. Ambas deben poder
explicar por qué falla la prueba y cómo se corrige.

Los comandos siguientes son para PowerShell, dentro del repositorio. Requieren
GitHub CLI autenticado (`gh auth status`) y acceso de escritura. Se fija `--repo`
para que GitHub CLI utilice esta copia y no el repositorio original del fork.
Para mostrar el botón de merge en el navegador, iniciar sesión como
`gabrielpaz2003` o como un colaborador con permiso de escritura. Una sesión
de otra cuenta sin ese permiso permite ver el PR, pero no integrarlo.
En Linux/macOS sustituir `.\.venv\Scripts\python.exe` por `.venv/bin/python`.

## 1. Mostrar el estado correcto

Abrir el repositorio, `mathlib/basic.py`, `tests/test_basic.py` y
`.github/workflows/tests.yml`. Mostrar Settings > Branches > protección de main:
check obligatorio **Pruebas unitarias**, rama actualizada e inclusión de
administradores.

```powershell
git switch main
git pull --ff-only origin main
.\.venv\Scripts\python.exe -m pytest -q
git log --oneline -8
```

Explicar: cada función tiene al menos dos escenarios exitosos y casos de error.
`pytest.raises` exige la excepción correcta, no cualquier valor de retorno.

## 2. Introducir el error en una rama

Comprobar que `git status --short` no muestra cambios propios pendientes.
Usar un nombre de rama nuevo en cada ensayo, por ejemplo `demo/en-vivo-01`.

```powershell
git switch -c demo/en-vivo-01
.\.venv\Scripts\python.exe scripts/demo_ci.py break
git diff -- mathlib/basic.py
.\.venv\Scripts\python.exe -m pytest -q
```

El fallo es deliberado: `square` retorna `n + n` en lugar de `n * n`.
`square(4)` retorna 8, pero la prueba exige 16. También fallan los casos de
entero negativo y decimal: resultado esperado **3 fallos y 74 aprobadas**.
No modificar ni eliminar las pruebas para ocultar el error.

```powershell
git add mathlib/basic.py
git commit -m "demo: introducir error intencional en square"
git push -u origin demo/en-vivo-01
gh pr create --repo gabrielpaz2003/AdminSP7 --base main --head demo/en-vivo-01 --title "Demo en vivo: fallo y correccion de square" --body "Demostracion de pruebas automaticas y bloqueo de merge."
gh pr view demo/en-vivo-01 --repo gabrielpaz2003/AdminSP7 --web
```

## 3. Mostrar el PR bloqueado

Esperar a que termine Actions. Abrir el detalle del check fallido y mostrar
el `AssertionError` de `test_positive_integer`: `assert 8 == 16`.

```powershell
gh pr checks demo/en-vivo-01 --repo gabrielpaz2003/AdminSP7 --watch
gh pr view demo/en-vivo-01 --repo gabrielpaz2003/AdminSP7 --json mergeStateStatus,statusCheckRollup
```

Explicar: el workflow corre por el evento `pull_request`; la regla de protección
es la que impide integrar el cambio. Mostrar **Merging is blocked**.
No usar privilegios de administrador para saltarse la protección.

## 4. Corregir el mismo PR

```powershell
.\.venv\Scripts\python.exe scripts/demo_ci.py fix
.\.venv\Scripts\python.exe -m pytest -q
git add mathlib/basic.py
git commit -m "fix: restaurar el calculo correcto de square"
git push
gh pr checks demo/en-vivo-01 --repo gabrielpaz2003/AdminSP7 --watch
```

Se esperan **77 aprobadas**. El nuevo commit actualiza el mismo PR, GitHub
Actions vuelve a ejecutar las pruebas y el check obligatorio cambia a verde.
Mostrar que el merge está habilitado y que ambos commits siguen visibles.

## 5. Integrar y cerrar

```powershell
gh pr merge demo/en-vivo-01 --repo gabrielpaz2003/AdminSP7 --merge
git switch main
git pull --ff-only origin main
```

El merge se realiza únicamente después de aprobar las pruebas. El historial
conserva el error deliberado y la corrección, mientras `main` queda funcional.

## Preguntas que conviene poder responder

- **¿Qué es integración continua?** Ejecutar validaciones automáticas con cada
  cambio que se propone integrar, para detectar regresiones pronto.
- **¿Qué diferencia hay entre Git y GitHub Actions?** Git registra versiones;
  Actions ejecuta los pasos automatizados definidos en el repositorio.
- **¿Una prueba fallida bloquea por sí sola el merge?** Hace falta configurar el
  check como obligatorio en la protección de `main`.
- **¿Por qué rechazar bool?** Python lo considera una subclase de `int`, pero el
  contrato de estas funciones pide números, no valores lógicos.
- **¿Por qué no comprobar solamente square(2)?** El error `n + n` también daría
  4; usar varias entradas permite detectar una implementación incorrecta.
- **¿Cómo sabemos que las demás funciones también están protegidas?**
  `scripts/check_mutations.py` rompe cada una en una copia temporal y confirma
  que sus pruebas fallan. No garantiza ausencia absoluta de errores, pero
  verifica los cinco defectos intencionales seleccionados.

## Entrega

En Canvas se entrega el enlace `https://github.com/gabrielpaz2003/AdminSP7`.
La actividad está configurada para cargar archivos: se puede entregar un PDF
breve con ese enlace, en lugar de un ZIP del código.
El README incluye los enlaces a código, pruebas, workflow y evidencias. La
presentación en clase sigue siendo necesaria aunque el enlace ya se haya
entregado.
