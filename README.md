# testing_kkrieger

---

Скрипт, целью которого является снятие статистики с игры kkrieger.
На время выполнения тестового задания под рукой был ноутбук с Ubuntu, поэтому пришлось воспользоваться Wine(обычно уже есть в штатных репозиториях Ubuntu,
но ссылку на программу оставлю ниже)

В скрипте используется multiprocessing для запуска двух процессов, первый запускает через wine игру kkrieger и снимает fps в выбранную пользователем 
директорию, второй процесс снимает скриншоты и с помощью opencv пропускает заставки, загружает сцену, заставляет идти персонажа до первого препятсвия.

Как это работает(в идеале):
Запуская скрипт, запускается игра через wine и пишет в лог количество кадров в секунду, который сохранется в директорию вывода указанную в команде 
запуска скрипта. С первых секунд снимаются скриншоты один за другим и сравниваются, это нужно чтобы скорее перейти от меню к сцене. 
После перехода в сцену снимается скриншот начальной сцены, который помещается также в директорию вывода. Персонаж перемещается вперед и снова запускается
цикл снятия скриншотов и их сравнивания, но уже для того, чтобы понять что персонаж застрял. Как только это случилось снимается скриншот конечной сцены, 
процесс wine закрывается, рассчитывается средний fps и весь вывод сохраняется.

Так как написан он был на скорую руку и с библиотекой opencv работать не приходилось, существует бесконечное пространство для тестирования и оптимизации :)
Запуск осуществляется командой типа: python3 main.py 'полный путь до exe kkrieger' -o 'полный путь до желаемой директории вывода'
Например: python3 main.py 'home/alexey/Загрузки/pno0001.exe' -o 'home/alexey/PycharmProjects/testing_kkrieger/output'

Тестировалось пока только на Ubuntu, вылеты довольно редкие, но бывали и в основном могут быть связаны с программой wine, которая, как известно, 
не всегда работает стабильно, поэтому иногда необходимо повторно запустить скрипт.

Ссылка на приложение wine:
https://www.winehq.org/
