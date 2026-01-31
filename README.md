# Hexlet Code: Page Loader

[![Actions Status](https://github.com/TonyYao0/python-pytest-testing-project-79/actions)

**Page Loader** — это консольная утилита для скачивания страниц из сети и их локального просмотра. Она загружает HTML-файл и все связанные локальные ресурсы (картинки, стили, скрипты), автоматически обновляя пути для автономной работы.

## Возможности

- Скачивание HTML-страницы и ресурсов в автоматическом режиме.
- Трансформация имен файлов (удаление схемы, замена спецсимволов на дефисы).
- Корректная замена путей в HTML на относительные локальные пути.
- Логирование процесса работы.

## Демонстрация (Installation & Usage)

[![asciicast](https://asciinema.org)](https://asciinema.org/a/qzaGQXPkeV0nJIzi.svg)
[![asciicast](https://asciinema.org)](https://asciinema.org/a/gYMnkgG346iwPRvR.svg)

## Установка

Проект использует менеджер пакетов [uv](https://astral.sh).

```bash
## Клонирование репозитория
git clone https://github.com/TonyYao0/python-pytest-testing-project-79.git
cd python-pytest-testing-project-79

## Сборка и установка пакета
make build
make package-install
