# Problemas-Olimpiadas | Matemáticas Fase 6

Banco de problemas para docentes de secundaria: 1,433 reactivos, 14 contenidos, 72 PDA y 1,472 asociaciones sugeridas. Fuente: Problemas_Contenidos_y_PDA_Fase6_NEM_Actualizado-v7.docx. Las asociaciones específicas son sugerencias, no asignaciones oficiales ni validadas individualmente. No contiene soluciones ni las figuras ausentes del original. Verificar permisos de redistribución de las fuentes antes de difundir.

## Estructura
- `database/banco_sqlite.sql`: fuente de verdad SQL relacional, con datos y vistas.
- `database/*.csv`: instantáneas de las cuatro tablas principales, compatibles con Excel.
- `src/index.template.html`: interfaz de búsqueda.
- `scripts/build.py`: reconstruye SQLite y el sitio estático a partir de SQL y comprueba integridad.
- `public/index.html`: buscador autónomo listo para abrir.
- `netlify.toml`: configuración del despliegue.

## Desarrollo y despliegue
Ejecutar `python3 scripts/build.py` para obtener `database/banco.sqlite` y regenerar el HTML. Abrir `public/index.html` o ejecutar `python3 -m http.server 8000 --directory public`.
En Netlify importar el repositorio pinchibeto-create/Problemas-Olimpiadas, rama main. Comando: `python3 scripts/build.py`. Carpeta: `public`. La configuración está incluida.

## Alcance
Las cuatro tablas de datos y los enunciados se recuperaron íntegramente del buscador previo. Se mantiene el conteo de 119 duplicados excluidos, pero no se incluye su registro detallado en esta exportación. El archivo binario SQLite se genera al construir el proyecto; no está incluido en este commit. Actualizar el SQL como fuente de verdad y regenerar las instantáneas CSV cuando cambien los datos. El HTML incorpora los datos y es accesible a cualquier visitante cuando el sitio es público; no es una base editable en tiempo real.

## Consulta de ejemplo
```sql
SELECT problema_id, texto, nivel FROM v_problemas_por_pda WHERE pda_id='C03-P04';
```
