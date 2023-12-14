Скрипт для парсинга архива погоды с сайта pogoda21.ru

## Установка
1. Установить python версии 3.0+
2. Склонировать репозиторий
3. Открыть терминал и перейти в корень склонированного репозитория
4. Создать виртуальное окружение
```
python -m venv env
```
5. Установить браузеры
```
playwright install
```
6. Установить зависимости
```
env\Scripts\pip install -r requirements.txt
```
7. Запустить программу с параметрами или без
```
python scraper.py
```
```
-s или --start - год начала для сбора данных
-e или --end - год конца сбора данных
-o или --output - путь сохранения выходного файла
```
