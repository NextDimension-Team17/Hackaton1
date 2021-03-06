# Создание набора данных для построения индивидуальной траектории обучения. 
Команда #17: Next Dimension онлайн-дататона магистратуры "Наука о данных" МИСИС, 19-24 октября 2020 г.

## Авторы
Дмитрий Малышев - Product Owner

Марина Беляева - Project Manager, 

Евгений Влащенков - Data Researcher+Visualization, 

Николай Фардзинов - бизнес-аналитик, 

Игорь Скороходов - разработчик, 

Павел Озернов - технический писатель

## Описание
Датасет содержит ссылки на статьи в "[интернет-энциклопедии Wikipedia](https://ru.wikipedia.org)" на русском языке, 
отобранные по принципу вложенности и релевантности предметной области "[Машинное обучение](https://ru.wikipedia.org/wiki/%D0%9C%D0%B0%D1%88%D0%B8%D0%BD%D0%BD%D0%BE%D0%B5_%D0%BE%D0%B1%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5)"
и "[Биоинформатика](https://ru.wikipedia.org/wiki/%D0%91%D0%B8%D0%BE%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B0)". 
Каждый уровень вложенности включает все ссылки основного текста статьи кроме ссылок в разделах "Литература" и "Примечание". 
Глубина вложенности - 10-15 уровней. Некоторые нерелевантные ссылки (например, ссылки на даты или дополнительные материалы в примечании) удалены, а дублирующие не использовались при визуализации.
Структура датасета - дерево с основной parent статьей "[Машинное обучение](https://ru.wikipedia.org/wiki/%D0%9C%D0%B0%D1%88%D0%B8%D0%BD%D0%BD%D0%BE%D0%B5_%D0%BE%D0%B1%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5)"
или "[Биоинформатика](https://ru.wikipedia.org/wiki/%D0%91%D0%B8%D0%BE%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B0)". 

Размер дататсета порядка 11000, но для визуализации используются около 2500, остальные являются дублирующими по полю title. В набор датасета включена полная визуализация в формате .png. Пример визуализации (неполная): ![](src/Tree_Example_-_Google_Chrome_2020-10-22_21.13.55.png)

## Источники
В качестве источника данных использовалась "[интернет-энциклопедия Wikipedia](https://ru.wikipedia.org)" на русском языке.

## Методы сбора и обработки
Формирование датасета последней MVP-версии производилось по состоянию на 23 октября 2020 г. методом парсинга вложенных ссылок в теле текущей статьи на 
другие релевантные рассматриваемой теме статьи. Парсинг осуществлялся с использованием библиотеки 
"[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)" для Python. 
Алгоритм парсинга включает некоторые условия фильтрации нерелевантных ссылок, позволяющих частично исключить их из датасета. Файлы исходного кода включены в датасет. 
Для визуализации использовалась "[Javascript-библиотека D3](https://d3js.org/)", в частности, примеры из статьи 
"[Tree diagrams in d3.js](http://www.d3noob.org/2014/01/tree-diagrams-in-d3js_11.html)" и 
"[NetworkX](https://networkx.org/documentation/stable/tutorial.html)".

## Структура репозитория
"[Каталог](https://github.com/NextDimension-Team17/Hackaton1/)" содержит файлы исходного кода Python в формате .py, папку "[data](https://github.com/NextDimension-Team17/Hackaton1/tree/main/data)" с файлом датасета в формате .csv и файлами визуализации в формате .png.

Датасет в формате .csv содержит следующие поля: 
* parent_title - название parent статьи
* title - название статьи
* parent_url - url parent статьи  
* url - url статьи


