---
date: 2019-02-05 17:01:11+00:00
images:
- url: /assets/images/1333.jpg
link_previews:
- description: This video presents an overview of new features and functions for ANSYS
    Mechanical 2019 R1.
  image: https://i.ytimg.com/vi/24WNCd3mxyA/maxresdefault.jpg?sqp=-oaymwEmCIAKENAF8quKqQMa8AEB-AH-CYAC0AWKAgwIABABGGUgZShYMA8=&rs=AOn4CLCYdvo7_QsYsrt4diSQ_jqPuJaV6A
  title: New Features and Capabilities for ANSYS Mechanical 2019 R1
  url: https://www.youtube.com/watch?v=24WNCd3mxyA
original_url: https://t.me/MagicDPD/1333
source: tg
title: Что нового в ANSYS Mechanical 2019R1
---

Давайте поговорим о новом релизе ANSYS, который получил коммерческое название 2019R1 и технический номер 19.3. ANSYS заботливо выложил видео с новыми фишками данного релиза, и я наконец могу про него поговорить.



  https://www.youtube.com/watch?v=24WNCd3mxyA



По традиции я бы хотел отметить те нововведения, которые зацепили меня. Таких набралось три штуки:



  Semi-implicit — (это просто бомба) полунеявный метод расчета. Решатель Mechanical ADPL теперь может переходить на явную схему интегрирования по времени (и возврящаться на неявную) при проблемах сходимости и когда шаг по времени уже итак очень мал. И так он может скакать десятки раз за расчет. Такого не делал еще никто.
  Contact split — опять наверно одним из первых неявный решатель ANSYS получил возможность обрабатывать одну контактную пару несколькими вычислительными потоками. Раньше «так носили» только explicit решатели. Традиционные же коды обрабатывали контакт одним ядром, что приводило к падению
