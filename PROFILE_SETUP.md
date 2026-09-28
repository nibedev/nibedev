# Mantener el perfil de GitHub

Este repositorio muestra el README del perfil **nibedev**.

## Actualizar textos, colores o botones

1. Edita `scripts/profile_assets.html`. Ahí están el saludo, las cuatro áreas de trabajo, las etiquetas de tecnologías y los botones.
2. En Windows, ejecuta `python scripts/render_profile_assets.py` desde la carpeta del repositorio. Necesitas Python con Pillow y Microsoft Edge. El script genera los PNG de `assets/` con DM Sans e Instrument Serif.
3. Revisa `README.md` y las imágenes generadas antes de publicar los cambios.

Los colores principales reflejan nibe.dev: fondo `#111415`, texto `#edece7` y azul `#b8d1e2`. El amarillo `#f5d547` se reserva para “design” y “videogames”. Los archivos de fuentes y sus licencias están en `assets/fonts/`.

## Actualizar enlaces y proyectos

- Los enlaces del portafolio, LinkedIn, Dribbble y Behance están en `README.md`.
- Los proyectos fijados debajo del README se administran desde el perfil de GitHub, en **Customize your pins**. No son parte de este archivo.
- La imagen de perfil y la biografía lateral también se editan desde GitHub, en **Edit profile**.
- El gato animado está en `assets/cat-animated.gif` y conserva su archivo por separado para que siga animado.

## Publicar con GitHub Desktop

Abre esta carpeta en GitHub Desktop, revisa los cambios, escribe un resumen, pulsa **Commit to main** y luego **Push origin**. Espera a que aparezca la versión nueva en https://github.com/nibedev.
