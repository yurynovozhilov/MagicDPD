---
date: 2019-06-10 17:00:30+00:00
images:
- url: /assets/images/1502.jpg
link_previews:
- description: ''
  image: http://yourmine.ru/i/parking/glob_parking.png
  title: "Ð¡Ñ\x80Ð¾Ðº Ñ\x80ÐµÐ³Ð¸Ñ\x81Ñ\x82Ñ\x80Ð°Ñ\x86Ð¸Ð¸ Ð´Ð¾Ð¼ÐµÐ½Ð° magicdpd.ru
    Ð¸Ñ\x81Ñ\x82Ñ\x91Ðº"
  url: https://wp.me/p9vWYY-2yI
original_url: https://t.me/MagicDPD/1502
source: tg
title: Расчеты в LS-DYNA на кластерах Windows HPC Cluster
---

DYNAmore выпустили инструкцию по настройке и работе распределённого решетеля LS-DYNA на кластерах под управлением MS Windows HPC Pack 2016. Инструкция полезная, но на самом деле вам достаточно знать следующий набор команд:



SET LSTC_MEMORY=auto
job submit /jobname: /numcores: /workdir:  mpiexec -np   i= jobid= 



Ну а если вы используете лицензии ANSYS LS-DYNA, то в начало надо добавить еще такое:



set LSTC_LICENSE=ANSYS
 set ANSYSLMD_LICENSE_FILE=1055@
 set ANSYSLI_SERVERS=2325@



Исходный документ тут: https://project.dynamore.se/public/windowscluster12

#HPC #LS_DYNA #MPI #Windows

https://wp.me/p9vWYY-2yI

by Юрий Новожилов
