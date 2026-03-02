---
layout: post
title: "LS-DYNA R10 - теперь официально"
date: 2017-08-02T09:00:11+00:00
author: "GlukRazor"
source: vk
original_url: https://vk.com/wall-97265142_424
tags:
  - ALE
  - DEM
  - LSDYNA
  - FSI
  - ICFD
  - SALE
---

http://www.dynasupport.com/news/ls-dyna-r10.0.0-r10.118302-released

#LSDYNA R10 теперь официально доступна. Есть и первый release note, который мы можем прочитать вместе. Вот, что я отметил из интересного для себя:
- Возможность на лету скармливать HEX #ALE сетку #SALE решателю
- Куча вкусностей для PARTICLE_BLAST
- CONTACT_AUTOMATIC_SURFACE_TO_SURFACE_MORTAR_TIED_WELD для моделирования сварки по критерию нагрева и касания
- При расчет пружинения учет износ поверхности - геометрия модифицируется решателем с учетом изношенности автоматически.
- CONSTRAINED_BEAM_IN_SOLID теперь работает для случаев динамической сеточной адаптации solid сетки, умеет делать армирование в tshell элементах.
- CONTROL_FORMING_SHELL_TO_TSHELL - конвертация shell (оболочек) в tshell (толстые оболочки) налету при штамповке и глубокой вытяжке
- Учет износа и эрозии при взаимодействии #DEM с сеточными телами.
- Адаптативное сеткоперестроение для PART_STACKED_ELEMENTS (моделирование композитов)
- Куча новшеств в #ICFD: простой рестарт, учет демпфирования, стационарная постановка, Windkessel boundary conditions
- Двухсторонний #FSI ICFD-DEM
- Доработки материала MAT_CONCRETE_EC2
- Опция AFTERBURN для EOS_JWL

Еще есть много всего для CASE и химического решателя, но ими я пока не пользовался, так что комментировать не могу.

Решатели лежат тут:
http://ftp.lstc.com/user/ls-dyna/R10.0.0/
http://ftp.lstc.com/user/mpp-dyna/R10.0/

Лицензии ANSYS LS-DYNA для 18.1 вполне хватает для запуска решателя.
