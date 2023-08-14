Restaurant-FastAPI
==================

- Для запуска приложения необходимо создать .env файл с переменными окружения как в файле .env.example
- create an **.env** file like **.env.example** file and fill it with your own values.

To run the project using docker-compose, run the following command:

```bash
docker compose up --build -d
```

To test the project, run the following command:

```bash
docker compose -f .\docker-compose.test.yml up --build --abort-on-container-exit
```

## Сделанные задания со звездочкой:

### ДЗ №2

##### **Реализовать вывод количества подменю и блюд для Меню через один (сложный) ORM запрос.**

- repositories.menu_repository

##### Реализовать тестовый сценарий « **Проверка кол-ва блюд и подменю в меню** » из Postman с помощью pytest

- tests.integration.menu_crud
- tests.integration.submenu_crud
- tests.integration.dish_crud
- tests.integration.computed_fields

### ДЗ №4

##### Блюда по акции. Размер скидки (%) указывается в столбце G файла Menu.xlsx

Для блюда отображается цена со скидкой
