# Анализ переводов

**views**
- *main_page* - получает данные и возвращает JSON с ключами:
    - greeting - получает данные из функции greeting.
    - cards - получает данные из функции get_cards_info.
    - top_transactions - получает данные из функции get_top_transactions.
    - currency_rates - получает данные из функции get_user_prefer_rates.
    - stock_prices - получает данные из функции get_user_stocks.
- *greeting* - приветствие в зависимости от времени суток (добрый день/утро/вечер/ночь).
- *get_cards_info* - возвращает список номеров карт и сумму потраченных средств за месяц указанной даты.
- *get_top_transaction* - возвращает топ 5 транзакций за месяц по указанным данным.
- *get_user_prefer_currency_rates* - возвращает курсы валют, перечисленные в файле user_setting, за текущий день.
- *get_user_stocks* - возвращает цены акций S&P500 за текущий день. Необходимо получить API-ключ с 'https://financialmodelingprep.com', создать файл '.env' и добавить в него строку 'APISP500=yourapikey', где 'yourapikey' нужно заменить на выданный ключ с 'financialmodelingprep.com'.

**utils**
- *read_excel* - получает данные в формате Pandas DataFrame из файла Excel.
- *get_user_settings* - получает настройки пользователя из файла JSON.
- *get_date* - преобразует дату из строки в формат datetime.date.
- *exchange* - конвертирует валюту в рубли ('RUB').
- *get_currency_rates* - декоратор для API получения курсов валют.
- *get_currency_rates_by_cbr* - получает курсы валют с API ЦБ РФ (Центрального банка России) в формате XML.
- *mask_card* - возвращает последние 4 цифры номера банковской карты.

**services**
- *search_individual_transfers* - получает транзакции переводов физическим лицам в формате JSON.

**reports**
- *write_report* - декоратор для записи данных отчета в файл JSON.
- *spending_by_category* - генерирует отчет о расходах по категориям за 3 месяца.

**test**
- *различные тесты для всех функций*