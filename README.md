# Лабораторная работа № 9

GitHub Actions запускает 12 UI-тестов калькулятора доставки при push, при открытии и обновлении pull request и вручную через вкладку Actions. Тесты выполняются в Chromium на Ubuntu с Python 3.11.

## Как запустить локально

В корне репозитория создайте виртуальное окружение и установите зависимости. Пример для macOS и Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium
python -m http.server 8000 --bind 127.0.0.1
```

В Windows создайте окружение командой `py -m venv .venv` и используйте `.venv\Scripts\python.exe` вместо `python` для остальных команд. Если в Linux отсутствуют системные библиотеки, выполните `python -m playwright install --with-deps chromium`.

Во втором терминале откройте тот же каталог и активируйте окружение. Выполните:

```bash
python -m pytest -v --browser chromium --screenshot only-on-failure --tracing retain-on-failure --output test-results --junitxml=report.xml
```

## Проверка в Actions

1. Отправьте проект в основную ветку. В **Actions → Playwright UI tests → ui-tests** проверьте шаги **Show Python version** и **Run UI tests**. Для исходной версии ожидается `12 passed`.
2. В `delivery.html` замените только `value >= 10000` на `value > 10000`, зафиксируйте изменение и отправьте его. На сумме ровно 10000 ₸ должны упасть TC03 (город) и TC07 (регион). Ожидаемый итог — `2 failed, 10 passed`, статус job — `failure`.
3. Верните `value >= 10000` и отправьте исправление. Проверьте восстановление `12 passed`.
4. От исправной версии создайте отдельную ветку, внесите небольшое изменение в README и откройте pull request. В Actions проверьте запуск с событием `pull_request`, в PR откройте **Checks**.

На странице каждого запуска в **Artifacts** доступен архив **ui-test-results**, если шаг загрузки выполнился. В нём `report.xml` содержит результаты тестов, `server.log` — запросы к форме. При падениях в `test-results/` сохраняются снимки экранов и трассировки. Трассировку можно открыть командой `python -m playwright show-trace путь/к/trace.zip`.


При открытии pull request GitHub Actions проверяет все 12 сценариев формы доставки.
