# Mantener el perfil de GitHub

Este repositorio muestra el README del perfil **nibedev**.

## Actualizar textos, colores o botones

1. Edita `scripts/profile_assets.html` para PC y `scripts/profile_assets_mobile.html` para celular. Ambos contienen el saludo, las áreas de trabajo, las tecnologías y los botones.
2. En Windows, ejecuta `python scripts/render_profile_assets.py` desde esta carpeta. Necesitas Python con Pillow y Microsoft Edge. El script genera los PNG transparentes de `assets/` para PC y celular, en temas claro y oscuro, con DM Sans e Instrument Serif. Los archivos terminados en `-mobile.png` son para celular y los terminados en `-light.png` son para el tema claro.
3. Revisa `README.md` y las imágenes generadas tanto en PC como a un ancho de celular antes de publicar. Los elementos `<picture>` seleccionan los recursos según el ancho de pantalla y el tema.

Los gráficos no incluyen un fondo sólido: dejan ver el fondo del tema de GitHub. En el tema oscuro, el texto usa `#edece7` y el acento azul usa `#b8d1e2`, como nibe.dev. En el tema claro se usan tonos más oscuros para mantener la legibilidad. Los recuadros grises de cada tecnología son parte de los iconos. Los archivos de fuentes y sus licencias están en `assets/fonts/`.

## Actualizar el gato

`assets/cat-transparent.gif` es la versión animada que usa el README. Si cambias el GIF de origen `assets/cat-animated.gif`, ejecuta `python scripts/make_cat_transparent.py` para quitarle el fondo y conservar la animación.

## Actualizar enlaces y proyectos

- Los enlaces del portafolio, LinkedIn, Dribbble y Behance están en `README.md`.
- Los proyectos fijados debajo del README se administran desde el perfil de GitHub, en **Customize your pins**. No son parte de este archivo.
- La imagen de perfil y la biografía lateral se editan en GitHub, en **Edit profile**.

## Publicar con GitHub Desktop

Abre esta carpeta en GitHub Desktop, revisa los cambios, escribe un resumen, pulsa **Commit to main** y luego **Push origin**. Espera a que aparezca la versión nueva en https://github.com/nibedev.
