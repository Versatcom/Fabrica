# CI/CD - Diseño y configuración

## Herramienta seleccionada
Se utiliza **GitHub Actions** para la orquestación CI/CD. La configuración vive en `.github/workflows/ci-cd.yml`.

## Pipeline por entorno
Los entornos se resuelven por rama:

- `develop` → **dev**
- `staging` → **staging**
- `main` → **prod**

### Pasos estándar por entorno
1. **Build**: `scripts/build.sh`
2. **Test**: `scripts/test.sh`
3. **Lint**: `scripts/lint.sh`
4. **Security scan**: `scripts/security_scan.sh`

## Despliegue automático
El job de despliegue ejecuta `scripts/deploy.sh` y aplica IaC desde `infra/`.

- IaC: Terraform (archivo base en `infra/main.tf`).
- Script de despliegue: `scripts/deploy.sh <environment> <strategy>`.

## Estrategias de release y rollback
- **Blue/Green** y **Canary** están soportadas como estrategias de despliegue en el script.
- El rollback se realiza revertiendo el tráfico al deployment anterior en el mismo flujo (definido en el script como placeholder para el proveedor cloud).

## Accesos y secretos
- Los secretos se gestionan en GitHub Actions → *Settings → Secrets and variables → Actions*.
- Recomendado:
  - `CLOUD_PROVIDER_CREDENTIALS`
  - `TERRAFORM_BACKEND_CONFIG`

## Ejecución manual
Se habilita `workflow_dispatch` para ejecutar el pipeline manualmente desde GitHub Actions.
