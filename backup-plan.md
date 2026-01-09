# Plan de infraestructura y respaldo

## 1. Proveedor cloud y región primaria
- **Proveedor seleccionado:** AWS.
- **Región primaria:** `us-east-1` (N. Virginia), con opción de DR en `us-west-2`.

## 2. Arquitectura base
- **Red (VPC):**
  - VPC /16 dedicada para el entorno productivo.
  - Subredes públicas (load balancers, NAT) y privadas (app y DB).
- **Subredes:**
  - 2 subredes públicas en AZ distintas.
  - 2 subredes privadas para cómputo.
  - 2 subredes privadas para base de datos.
- **Balanceadores:**
  - Application Load Balancer (ALB) en subredes públicas.
- **Cómputo:**
  - Auto Scaling Group de instancias EC2 en subredes privadas.
  - (Alternativa) ECS/Fargate si se desea contenedores.
- **Base de datos gestionada:**
  - Amazon RDS (PostgreSQL/MySQL) con Multi-AZ.

## 3. Políticas de backup y retención
- **Base de datos (RDS):**
  - Backups automáticos diarios.
  - Retención de 30 días.
  - Snapshots manuales antes de cambios mayores.
- **Almacenamiento de archivos (S3/EFS):**
  - Versionado habilitado en buckets S3.
  - Lifecycle policies para mover a Glacier después de 30 días.
  - Retención mínima de 90 días en Glacier.

## 4. Monitoreo y alertas
- **CloudWatch / AWS Backup:**
  - Alarmas por fallos de backup y expiraciones.
  - Notificaciones vía SNS (email/Slack).
  - Dashboard de estado de backups.

## 5. Procedimiento de restore y pruebas
- **Restore de base de datos:**
  1. Identificar snapshot o punto en el tiempo.
  2. Restaurar a instancia nueva.
  3. Validar integridad y pruebas de lectura/escritura.
- **Restore de almacenamiento:**
  1. Recuperar versión desde S3.
  2. Validar checksum y consistencia.
- **Pruebas periódicas:**
  - Simulacro trimestral de restauración.
  - Reporte con tiempos RTO/RPO reales.
