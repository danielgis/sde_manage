# SDEManager

Es una herramienta que automatiza el proceso de mantenimiento de bases de datos espaciales corporativas (Enterprise Geodatabase) de tecnología ESRI. Esta desarrollada integramente en Python27 y hace uso de la librería arcpy de ArcGIS. Ejecuta los procesos siguientes:

* **Bloqueo de conexiones:** a la base de datos corportativa.
* **Desconexión de usuarios:** necesario para proceder con la compresión de la base de datos.
* **Compresion de la base de datos:** esto elimina los registros huerfanos de las tablas alfa y delta en una geodatabase versionada.
* **Reconstrucción de indices:** necesario ya que los indices se fragmentan al realizarse la compresion de base de datos. Este proceso incluye a las tablas del sistemas las cuales son las tablas de linaje como states, state_lineages y mv_tables_modified en SQLServer.
* **Análisis de Datasets:** permite actualizar las estadísticas de la base de datos.
* **Habilitar las conexiones:** permite nuevamente el uso de la base de datos corporativa para los usuarios.

## Considerar
* Es necesario realizar el proceso de conciliación de base de datos con las otras versiones existentes para evitar conflictos.
* El proceso reconstruye los indices y las estadísticas de las tablas que son propiedad del usuario registrado como administrador en el ArcSDE

## Dependencias
    arcpy
    pandas
    uuid*
    os*
    inspect*
    sqlite3*
    
> '*' Son librerias estandar de Python27

## Créditos
* [danielgis](https://danielgis.github.io)