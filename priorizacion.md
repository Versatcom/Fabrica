# Criterios de decisión y priorización

## Criterios de decisión
1. **Impacto en el negocio**
   - Evalúa el efecto esperado en ingresos, retención y ventaja competitiva.
   - Métrica base: impacto estimado en ingresos anuales y usuarios afectados.

2. **Costo total**
   - Considera costos de desarrollo, licencias, infraestructura y operación.
   - Métrica base: costo total estimado (CAPEX + OPEX) para implementar y operar.

3. **Riesgo técnico**
   - Evalúa complejidad técnica, dependencias críticas y probabilidad de fallas.
   - Métrica base: nivel de incertidumbre técnica y esfuerzo de mitigación.

4. **Time-to-market**
   - Evalúa el tiempo para entregar valor al cliente.
   - Métrica base: semanas estimadas para entrega a producción.

## Evidencia usada
- **Costos** (estimaciones internas):
  - Desarrollo: 6 semanas con 4 personas (24 persona-semanas) a 1.200 USD/semana = 28.800 USD.
  - Licencias: 8.000 USD/año.
  - Infraestructura: 1.500 USD/mes.
- **Tiempos** (estimaciones del equipo):
  - Diseño + build + QA: 8 semanas.
  - Integración y despliegue: 2 semanas.
- **Capacidad** (planificación trimestral):
  - Equipo disponible: 4 FTE, 70% de capacidad asignable en el trimestre.
- **Riesgo** (matriz de riesgos):
  - Dependencia de API externa con SLA 99,5%.
  - Complejidad de migración de datos media.

## Priorización final y justificación
### Criterio: Impacto en el negocio
- **Prioridad**: Alta
- **Justificación**: El incremento esperado de ingresos (120.000 USD/año) y la mejora en retención (+3%) afectan directamente los OKR del trimestre.

### Criterio: Costo total
- **Prioridad**: Media
- **Justificación**: El costo total anual (28.800 USD + 8.000 USD + 18.000 USD de infraestructura) es manejable, pero requiere alineación presupuestaria.

### Criterio: Riesgo técnico
- **Prioridad**: Media
- **Justificación**: La dependencia de API externa y la migración de datos agregan riesgo, aunque mitigable con pruebas y planes de contingencia.

### Criterio: Time-to-market
- **Prioridad**: Alta
- **Justificación**: La ventana de mercado es corta y las 10 semanas estimadas son compatibles con el calendario comercial.
