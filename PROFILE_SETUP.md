# Mantener el perfil de GitHub

Este repositorio muestra el README del perfil **nibedev**.

## Actualizar textos, colores o botones

1. Edita `scripts/profile_assets.html`. Ahí están el saludo, las cuatro áreas de trabajo, las tecnologías y los botones.
2. En Windows, ejecuta `python scripts/render_profile_assets.py` desde esta carpeta. Necesitas Python con Pillow y Microsoft Edge. El script genera los PNG transparentes de `assets/` para los temas claro y oscuro de GitHub, con DM Sans e Instrument Serif. Los archivos terminados en `-light.png` corresponden al tema claro.
3. Revisa `README.md` y las imágenes generadas antes de publicar.

Los gráficos no incluyen un fondo sólido: dejan ver el fondo del tema de GitHub. En el tema oscuro, el texto usa `#edece7` y el acento azul usa `#b8d1e2`, como nibe.dev. En el tema claro se usan tonos más oscuros para mantener la legibilidad. Los recuadros grises de cada tecnología son parte de los iconos. Los archivos de fuentes y sus licencias están en `assets/fonts/`.

## Actualizar el gato

`assets/cat-transparent.gif` es la versión animada que usa el README. Si cambias el GIF de origen `assets/cat-animated.gif`, ejecuta `python scripts/make_cat_transparent.py` para quitarle el fondo y conservar la animación.

## Actualizar enlaces y proyectos

- Los enlaces del portafolio, LinkedIn, Dribbble y Behance están en `README.md`.
- Los proyectos fijados debajo del README se administran desde el perfil de GitHub, en **Customize your pins**. No son parte de este archivo.
- La imagen de perfil y la biografía lateral se editan en GitHub, en **Edit profile**.

## Publicar con GitHub Desktop

Abre esta carpeta en GitHub Desktop, revisa los cambios, escribe un resumen, pulsa **Commit to main** y luego **Push origin**. Espera a que aparezca la versión nueva en https://github.com/nibedev.
