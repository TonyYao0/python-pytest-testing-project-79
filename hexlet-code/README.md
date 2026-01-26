# Hexlet Code: Page Loader

[![Actions Status](https://github.com)](https://github.com)
[![Maintainability](https://api.codeclimate.com)](https://codeclimate.com)
[![Test Coverage](https://api.codeclimate.com)](https://codeclimate.com)

**Page Loader** — консольная утилита для скачивания страниц из сети и их локального просмотра. Программа загружает HTML-файл и все связанные локальные ресурсы (картинки, стили, скрипты).

## Возможности

* Скачивает страницу и сохраняет её в указанную директорию.
* Изменяет ссылки в HTML на локальные пути.
* Сохраняет все локальные ресурсы в отдельную папку.
* Преобразует URL в безопасные имена файлов.
* Логирует процесс работы в консоль.

## Демонстрация установки и работы

[![asciicast](https://asciinema.org)](https://asciinema.org)

## Установка

Для установки необходим Python 3.10+ и менеджер пакетов [uv](https://astral.sh).

```bash
# Клонирование репозитория
git clone https://github.com/TonyYao0/python-pytest-testing-project-79
cd python-pytest-testing-project-79

# Сборка и установка
make build
make package-install
