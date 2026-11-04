<!-- LANG-BAR -->
[English](CONTRIBUTING.md) · [한국어](CONTRIBUTING.ko.md) · [简体中文](CONTRIBUTING.zh-CN.md) · [日本語](CONTRIBUTING.ja.md) · **Español**
<!-- /LANG-BAR -->

# Guía de contribución

Este repositorio es una **especificación**, no una implementación. Las contribuciones son de tres tipos principales: cambios en el texto, cambios en los esquemas y ejemplos, y cambios en las reglas de la calculadora.

## Antes de empezar

```bash
pip install -r requirements.txt               # para check_schemas.py
python3 tools/design_space.py --check all     # P1~P7 deben ser todos clean
python3 tools/check_schemas.py                # la última línea debe ser ALL OK
```

Envía el PR con ambos comandos pasando. La enumeración completa (`python3 tools/design_space.py`) tarda unos minutos.

## Lo que hay que respetar

- **Los identificadores son un contrato entre archivos.** Los ejes `A1~A11`, las restricciones `L`/`N`/`S`, las invariantes `I1~I10`, los pisos `F1~F7`, las puertas `G0~G5`, los pasos de resolución `R0~R5`, los perfiles `P1~P7` y los modelos de negocio `B1~B20` aparecen a la vez en los documentos, los esquemas, `design_space.py` y `check_schemas.py`. No cambies ni borres números; añade los elementos nuevos al final. Para retirar uno, deja el número vacío y escribe "retirado".
- **Las cifras de los documentos son resultados de cálculo.** Si cambias `AXES` · `LOGICAL_RULES` · `normative()` · `soft()` · `BMS`, vuelve a ejecutar la herramienta y corrige todas las cifras en `README.md`, `docs/01`, `docs/03`, `docs/09` y `CHANGELOG.md`.
- **No cambies el orden de `LOGICAL_RULES`.** El recuento de "primera violación" depende del orden.
- **Los perfiles están en tres lugares**: `PROFILES` en `design_space.py`, `examples/profiles.yaml` y la tabla del README.
- **Si cambias la estructura de un ejemplo**, las rutas de mutación de `CASES` en `check_schemas.py` pueden desalinearse sin avisar. Comprueba que todas las pruebas de documentos prohibidos den `OK`.
- **Ediciones por idioma**: la edición coreana (`docs/ko/`, `*.ko.md`) es la original. Inglés (`docs/en/`, README predeterminado) · 简体中文 (`zh-CN`) · 日本語 (`ja`) · Español (`es`) son traducciones y usan los mismos nombres de archivo. Si modificas el original, corrige también las traducciones en el mismo PR o indica en la descripción del PR los idiomas que no pudiste corregir. No se traducen identificadores, cifras ni código. Las descripciones de los esquemas, los ejemplos y los mensajes de las herramientas se escriben en inglés.
- El texto se escribe en lenguaje sencillo. Niveles de requisito: DEBE (MUST) · DEBERÍA (SHOULD) · PUEDE (MAY). Las cifras sin fuente se marcan como **valor de diseño propuesto**. Para las fuentes, se prefieren las primarias ([docs/references.md](docs/es/references.md)).

## Issues · PR

- Indica en el título o en el cuerpo el capítulo y el id de regla correspondientes (p. ej., `3.3 L7`, `I10`, `6.5 R2`).
- Si te opones a una regla, la discusión avanza más rápido si muestras con `--profile` **una combinación que esa regla filtra por error**.
- Los cambios grandes (un eje nuevo, una invariante nueva, un cambio de contrato de esquema) propónlos primero en un issue. Si se incorporan, se registran en `CHANGELOG.md`.

## Licencia

Lo que aportes se rige por las licencias del repositorio. Los documentos (`docs/`, `README.md`, etc.) están bajo CC BY 4.0 ([LICENSE-docs](LICENSE-docs)), y los esquemas · ejemplos · herramientas (`schemas/`, `examples/`, `tools/`) bajo Apache-2.0 ([LICENSE](LICENSE)).
