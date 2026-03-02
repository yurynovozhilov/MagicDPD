---
date: 2019-02-08 06:49:21+00:00
images:
- url: /assets/images/1341.jpg
- url: /assets/images/1342.jpg
- url: /assets/images/1343.jpg
- url: /assets/images/1344.jpg
- url: /assets/images/1345.jpg
link_previews:
- description: ''
  image: http://yourmine.ru/i/parking/glob_parking.png
  title: "Ð¡Ñ\x80Ð¾Ðº Ñ\x80ÐµÐ³Ð¸Ñ\x81Ñ\x82Ñ\x80Ð°Ñ\x86Ð¸Ð¸ Ð´Ð¾Ð¼ÐµÐ½Ð° magicdpd.ru
    Ð¸Ñ\x81Ñ\x82Ñ\x91Ðº"
  url: https://wp.me/s9vWYY-4381
- description: ''
  image: http://yourmine.ru/i/parking/glob_parking.png
  title: "Ð¡Ñ\x80Ð¾Ðº Ñ\x80ÐµÐ³Ð¸Ñ\x81Ñ\x82Ñ\x80Ð°Ñ\x86Ð¸Ð¸ Ð´Ð¾Ð¼ÐµÐ½Ð° magicdpd.ru
    Ð¸Ñ\x81Ñ\x82Ñ\x91Ðº"
  url: https://wp.me/s9vWYY-4396
- description: ''
  image: http://yourmine.ru/i/parking/glob_parking.png
  title: "Ð¡Ñ\x80Ð¾Ðº Ñ\x80ÐµÐ³Ð¸Ñ\x81Ñ\x82Ñ\x80Ð°Ñ\x86Ð¸Ð¸ Ð´Ð¾Ð¼ÐµÐ½Ð° magicdpd.ru
    Ð¸Ñ\x81Ñ\x82Ñ\x91Ðº"
  url: https://wp.me/s9vWYY-4616
- description: ''
  image: http://yourmine.ru/i/parking/glob_parking.png
  title: "Ð¡Ñ\x80Ð¾Ðº Ñ\x80ÐµÐ³Ð¸Ñ\x81Ñ\x82Ñ\x80Ð°Ñ\x86Ð¸Ð¸ Ð´Ð¾Ð¼ÐµÐ½Ð° magicdpd.ru
    Ð¸Ñ\x81Ñ\x82Ñ\x91Ðº"
  url: https://wp.me/s9vWYY-5426
original_url: https://t.me/MagicDPD/1341
source: tg
title: Литеература по резанию металла на русском
---

Тот самый случай, когда лучший подарок — это книга!
Поздравляем наших коллег из Арзамасского политехнического института с выпуском отличного учебного пособия «Численное моделирование процессов резания».
В книге рассмотрены 3 метода моделирования процесса резания в программе LS-DYNA: Лагранжевый, SPH и EFG.
Приведена подробная последовательность действий для создания данных моделей в препроцессоре ls-prepost.
В конце книги представлены параметры уравнений и разрушений модели материала Джонсона-Кука для большого количества различных материалов.


#cut #EFG #LS_DYNA #SPH

https://wp.me/s9vWYY-4381

by GlukRazor

Повышение устойчивости SPH при помощи Moving Last Square подхода


На своем канале #LSTC показали несколько тестовых задач, демонстрирующих работу их новой формулировки для #SPH. Напомню, что SPH обладает врожденной болезнью: нестабильностью при работе на растяжение. Материал, моделируемый в SPH постановке показывает разрушение при растяжении намного раньше, чем того требуют его механическое состояние — получается так из-за численных проблем.
В видео от LSTC демонстрируется работа билда #LSDYNA с 12-ой формулировкой метода SPH, получившей название MLS-based. К сожалению, даже в самой свежей черновой документации от 4 октября, данная опция никак не описана. Однако удалось найти, что #MLS (moving last square) интерполяция ранее применялась в LS-DYNA для бессеточного метода Галеркина (#EFG, Element Free Galerkin), так что какое-то описание по теории работы метода все-таки можно найти.
Важно другое: когда MLS-based SPH войдет в очередной релиз — это будет большой шаг в области применения бессрочных методов для

Моделирование процессов ОМД на АО Ульяновский НИАТ


Приятно видеть, когда люди работают, и работают хорошо!
#LSDYNA #EFG #forming
Краткая статья про применение моделирования процессов на АО «Ульяновский НИАТ»
http://tzshp.ru/o-nas/stati/59-modelirovanie-protsessov-omd-na-ao-ulyanovskij-niat
Моделирование процессов ОМД на АО Ульяновский НИАТ
http://tzshp.ru/o-nas/stati/59-modelirovanie-protsessov-omd-na-ao-ulyanovskij-niat
Моделирование процессов ОМД на АО Ульяновский НИАТ

#EFG #forming #LS_DYNA

https://wp.me/s9vWYY-4396

by GlukRazor

Моделирование ковки


Cравнение различных подходов моделирования задачи ковки. Задача сопряжена с большими пластическими деформациями, которые неминуемо приводят к сеточным проблемам. Как раз для таких случаев есть #EFG метод, да еще и с несколькими стратегиями сгущения сетки.
#LSDYNA

 Cylinder forging with LS-DYNA

#EFG #forming #LS_DYNA

https://wp.me/s9vWYY-4616

by GlukRazor

r-adaptive Element-Free Galerkin


Резка металла может быть промоделирована неявным решателем LS-DYNA для адаптивной постановки бессеточного метода Галеркина (r-adaptive Element-Free Galerkin, EFG).
Сетка, которую вы видите — это не совсем сетка. Подробнее в прилагаемой презентации по данному бессеточному методу.
#EFG #implicit #lsdyna
 LS-DYNA: Implicit element-Free Galerkin (EFG) — Cutting Simulation

 Файл Element-Free Galerkin Method.pdf

#EFG #implicit #LS_DYNA

https://wp.me/s9vWYY-5426

by GlukRazor
