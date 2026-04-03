<h1 align="center">TimeDistancePlotBuilder ☀️ </h1>

# Оглавление

- [Введение](#введение)
- [Предназначение и использование программы](#предназначение-и-использование-программы)
- [Пример использования программы](#пример-использования-программы)
- [Примеры полученных результатов](#примеры-полученных-результатов)

## Введение

В настоящее время одними из объектов наблюдения, на которых сосредоточен интерес ученых в области физики Солнца, являются корональные петли. Корональные петли – один из доминирующих видов магнитных структур солнечной короны, отличающийся повышенной температурой и плотностью по отношению к окружающей плазме.

Наблюдение за эволюцией корональных петель позволяет извлечь информацию о проходящих в них процессах, которая полезна для решения “Проблемы коронального нагрева”. Данная проблема заключается в том, что внешняя атмосфера Солнца намного горячее его поверхности, хотя ожидается, что температура должна уменьшаться с расстоянием от ядра. До сих пор этот вопрос остается нерешенным. Оказалось, что наблюдаемые в солнечной атмосфере МА колебания и волн могут помочь пролить свет на этот вопрос и глубже понять процессы, происходящие в короне Солнца.

В изучении процессов корональных петель помогает Пространственно-временная диаграмма интенсивности (ПВДИ). Это разновидность двумерного графика, который показывает распределение интенсивности излучения вдоль петли в течении промежутка времени.

![Interface](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/Interface.png)

Данная программа предназначена для упрощения построения ПВДИ по имещюимся на компьютере FITS файлам. Для построения ПВДИ нужно выполнить следующий алгоритм:

## Процесс установки

- Создайте каталог в которую будет установлена программа. Поместите туда install.ps1. Данный скрипт скачает архив с последним билдом программы и тестовые изображения. Это может занять время!

- Запустите скрипт. Данный скрипт скачает последний билд программы и тестовые изображения солнца. Создаст ярлык на рабочем столе для запуска программы.

- Программу нужно запускать через ярлык или консоль

## Пример использования программы

Загрузка программы

![Interface](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/Loading.png)

Начальное состояние программы после загрузки для изображений в канале 131
![Interface](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/Interface.png)

Начальное состояние программы после загрузки для изображений в канале 171
![Interface](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/Interface2.png)

Выделенный участок в короне солнца
![Interface](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/Interface3.png)

Построенный ПВДИ по выделенной петле
![Interface](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/Interface4.png)

Построенный и оформленный график
![Interface](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/Interface5.png)

Окошко экспорта графика
![Interface](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/Interface7.png)

Окошко экспорта данных (изображение и массив numpy для дальнейшей обработки)
![Interface](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/Interface6.png)

Окошко экспорта изображения
![Interface](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/ExportPopup.png)

## Примеры полученных результатов

![A94](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/A94.png)
![A131](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/A131.png)
![A171](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/A171.png)
![A193](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/A193.png)
![A211](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/A211.png)
![A304](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/A304.png)
