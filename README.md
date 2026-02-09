The purpose of this script is to automate the generation of monthly warehouse reports. As a result of a sale, some items may not be written off for various reasons (e.g., sales without write-offs from the sales database (salesperson error), consumption of goods for personal needs, mis-sorting, etc.). This information is strategically important for every retailer to ensure the integrity and completeness of warehouse information.

**Task:** Find items whose quantities differ from the accounting database.

We have three tables from different departments at the end of the month:

`control` - inventory balance according to accounting, what should actually be there;
`storage1` - inventory balance in warehouse #1;
`storage2` - inventory balance in warehouse #2.

The product mix and quantity are extracted from the database. Some imbalances are intentionally introduced to demonstrate the script's functionality. The file names are universal and do not differ from month to month; only the contents change according to the reporting date.




Задача данного скрипта - автоматизировать составление ежемесячной отчетности по складу. В результате продажи, некоторые товары могут быть не списаны по разным причинам (например продажа без списания по торговой базе (ошибка продавца), потребление товара на собственные нужды, пересорт и тд.). Для целостности и полноты информации о складе, данная информация стратегически важна для каждого торгового предприятия.

**Цель:** найти товары, количество которых различатеся с бухгалтерской базой.

У нас есть 3 таблицы из разных отделов предприятия на конец месяца:

* `control` - остатки товара по бухгалтерии, то что должно быть фактически;
* `storage1` - остатки товара на складе №1;
* `storage2` - остатки товара на складе №2.

Набор и количество товара являются выборкой из базы данных. Некоторый дисбаланс внесен специально, с целью показать функциональность скрипта. Названия файлов универсальны и не отличаются от месяца к месяцу, меняется только содержимое согласно отчетной дате.