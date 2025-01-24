# Trazabilidad de Medicamentos

## Descripción del Módulo
El módulo de Trazabilidad de Medicamentos permite a las empresas gestionar la trazabilidad de productos farmacéuticos, integrando los sistemas de compras y ventas con un sistema externo mediante su API. Este módulo también incluye una Mock API para pruebas locales y proporciona herramientas para consultar y actualizar la trazabilidad de los productos.

## Características Principales
1. Sincronización con el sistema externo:
   - Enviar información de productos trazados al sistema externo tras una compra o venta.
   - Registrar la fecha e ID de procesamiento obtenido desde el sistema externo.

2. Gestión de productos trazados:
   - Menú para listar los productos trazados y los pendientes de trazabilidad.
   - Botones en el formulario para consultar y actualizar la trazabilidad.

3. Integración con Compras y Ventas:
   - Creación automática de registros de trazabilidad al confirmar ventas y compras.
   - Asignación de lotes o números de serie en la recepción.

4. Configuración flexible:
   - Opcion para cambiar la URL de la API.
   - Habilitar o deshabilitar el uso de la Mock API.

## ## Requisitos del Sistema

Para el correcto funcionamiento del módulo, asegúrate de cumplir con los siguientes requisitos:

- Odoo: Versión 16 Community, instalada y configurada.
- Base de datos: PostgreSQL (gestionada por Odoo).
- Python: Instalación compatible con la versión de Odoo utilizada.

## Instalación
1. Clona el repositorio o descomprime el archivo del módulo en tu carpeta de addons de Odoo:
2. Reinicia el servidor de Odoo:
3. Activa el modo desarrollador en Odoo.
4. Ve al menú Apps y actualiza la lista de módulos.
5. Busca "Trazabilidad de Medicamentos" e instálalo.

## Configuración
1. Ve al menú Configuración > Configuración de Trazabilidad.
2. Configura:
   - URL de la API: Cambia la URL del sistema externo si es necesario.
   - Usar Mock API: Actívala para pruebas locales.

## Uso del Módulo
### 1. Creación Automática de Trazabilidad
- Al confirmar una orden de compra o venta, se creará automáticamente un registro en Trazabilidad de Medicamentos sin un lote asignado.

### 2. Asignar Lotes
- En el menú de trazabilidad, se debe asignar el lote o número de serie al registro correspondiente antes de consultar la trazabilidad.

### 3. Consultar y Actualizar Trazabilidad
- En la vista formulario de Trazabilidad de Medicamentos:
   - Usa el botón "Consultar Trazabilidad" para obtener información inicial del sistema externo.
   - Usa el botón "Actualizar Trazabilidad" para actualizar el estado de un registro existente.

## Ejemplos de Configuración de la Mock API
La Mock API simula las respuestas del sistema externo para pruebas locales:

- Consultar trazabilidad:
   ```python
   {
       "processing_id": "123456",
       "status": "procesado"
   }
   ```

- Actualizar trazabilidad:
   ```python
   {
       "status": "procesado"
   }
   ```

## Propuesta de Mejoras
1. Agregar soporte para generar reportes detallados en PDF o Excel.
2. Incluir notificaciones automáticas para productos pendientes de trazabilidad.
3. Mejorar la integración con sistemas externos permitiendo configuraciones adicionales como claves API y autenticación.
