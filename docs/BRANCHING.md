# Estrategia de ramas — GitHub Flow

- `main`: siempre estable y desplegable. Protegida: solo se modifica mediante Pull Request aprobado.
- Ramas de trabajo (desde `main`, vida corta, una por historia o tarea):
  - `feature/HU-LP-01-consultar-inventario`
  - `fix/HU-LP-10-validar-stock`
  - `docs/readme-estructura`
  - `chore/docker-compose`
- Commits en imperativo con prefijo (`feat:`, `fix:`, `docs:`, `test:`, `chore:`) y el ID de la historia. Ej.: `feat(HU-LP-01): consultar existencias por almacén`.
- Pull Request: plantilla de `.github/`, enlaza historia(s), requiere al menos 1 revisión de otro integrante y se fusiona con *Squash and merge*. La rama se elimina tras el merge.
- Justificación: equipo pequeño, sprint de 2 semanas; GitHub Flow evita la complejidad de Gitflow.

## Plan de Pull Requests del Sprint 1
| PR | Rama | Historia |
|----|------|----------|
| PR-LP-01 | feature/HU-LP-01-consultar-inventario | HU-LP-01 |
| PR-LP-02 | feature/HU-LP-02-reglas-reposicion | HU-LP-02 |
| PR-LP-03 | feature/HU-LP-04-rastrear-envio | HU-LP-04 |
| PR-LP-04 | feature/HU-LP-07-registrar-telemetria | HU-LP-07 |
| PR-LP-05 | feature/HU-LP-10-crear-pedido | HU-LP-10 |
