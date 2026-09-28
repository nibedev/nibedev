# Publicar y mantener este perfil

Este repositorio contiene el README visual para el perfil de GitHub `nibedev`. Todos los recursos que se muestran están guardados aquí; el perfil no depende de un servicio de iconos externo. No contiene emojis.

## Primera publicación

1. Crea en GitHub un repositorio **público** llamado exactamente `nibedev`, bajo la cuenta `nibedev`.
2. Sube el contenido de esta carpeta a la rama principal de ese repositorio. GitHub mostrará automáticamente el archivo `README.md` en el perfil.
3. En **Settings → Public profile**, configura el nombre, biografía, pronombres, sitio web y enlace de LinkedIn como prefieras. La barra lateral de la maqueta pertenece al perfil de GitHub y no se puede modificar desde el README. Se incluye `assets/avatar.png` como propuesta de avatar basada en el GIF; puedes subirlo allí si te gusta.
4. En **Customize your pins**, fija `Tienda-Nivel-Retro` y `Namster-Cafe` si son públicos y aparecen en tu cuenta. Las tarjetas de la maqueta son los elementos nativos de GitHub; sus nombres, descripciones y visibilidad se administran en cada repositorio.

## Actualizar el contenido

- Textos, colores, nombres de herramientas y posiciones: edita `scripts/build_assets.py` y ejecuta `python scripts/build_assets.py` desde esta carpeta. Requiere Python 3 y Pillow (`python -m pip install Pillow`).
- GIF: reemplaza `3_Gato_acostado_FINAL.gif` por otra versión con el mismo nombre y vuelve a ejecutar el script. El original se conserva; `assets/cat-animated.gif` es una versión más ligera para el perfil.
- LinkedIn: cambia el enlace en `README.md` si tu dirección personalizada cambia.
- Dribbble y Behance: hoy son tarjetas visuales sin enlace. Cuando existan tus perfiles, cambia estas tarjetas por enlaces reales en `README.md` y actualiza `build_contact()` en el script para quitar «Coming soon».
- Avatar y datos de la barra lateral: cámbialos en la configuración de GitHub. El archivo `assets/avatar.png` no modifica el avatar por sí solo.
- Repositorios fijados: se actualizan desde la página de perfil de GitHub, no desde el README.

## Subir los cambios

Después de crear el repositorio público, conecta esta carpeta y publica:

```bash
git remote add origin https://github.com/nibedev/nibedev.git
git push -u origin main
```

Para cambios posteriores, vuelve a ejecutar el generador cuando corresponda, revisa los archivos, crea un commit y ejecuta `git push`.

## Alcance visual

GitHub decide el ancho de la columna, los bordes y las tarjetas nativas. El README reproduce la composición central de la maqueta; puede cambiar de tamaño o repartir las piezas en más líneas en pantallas pequeñas. Los gráficos usan un fondo oscuro propio para que el texto amarillo y blanco se mantenga legible incluso si alguien ve GitHub en modo claro.

## Iconos y licencias

- Logos de tecnologías y LinkedIn: [Devicon](https://github.com/devicons/devicon), licencia MIT en `assets/vendor/DEVICON-LICENSE.txt`.
- Iconos lineales de las cuatro áreas: [Lucide](https://lucide.dev/), licencia ISC en `assets/vendor/LUCIDE-LICENSE.txt`.
- Logos de AutoCAD, Dribbble y Behance: [Simple Icons](https://simpleicons.org/), licencia en `assets/vendor/SIMPLE-ICONS-LICENSE.txt`. Los nombres y marcas pertenecen a sus titulares.

Los SVG originales están en `assets/vendor/`; el script los integra en las imágenes finales. Revisa las políticas de cada marca antes de emplear estos logos en otros contextos.
