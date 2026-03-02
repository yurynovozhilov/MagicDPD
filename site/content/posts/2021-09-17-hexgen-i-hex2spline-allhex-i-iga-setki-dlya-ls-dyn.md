---
date: 2021-09-17 13:01:45+00:00
link_previews:
- description: In this paper, we present two software packages, HexGen and Hex2Spline,
    that seamlessly integrate geometry design with isogeometric analysis (IGA) in
    LS-DYNA. Given a boundary representation of a solid model, HexGen creates a hexahedral
    mesh by utilizing a semi-automatic polycube-based mesh generation method. Hex2Spline
    takes the output hexahedral mesh from HexGen as the input control mesh and constructs
    volumetric truncated hierarchical splines. Through Bézier extraction, Hex2Spline
    transfers s
  image: /static/browse/0.3.4/images/arxiv-logo-fb.png
  title: 'HexGen and Hex2Spline: Polycube-based Hexahedral Mesh Generation and Spline
    Modeling for Isogeometric Analysis Applications in LS-DYNA'
  url: https://arxiv.org/abs/2011.14213
- description: Contribute to yu-yuxuan/HexGen_Hex2Spline development by creating an
    account on GitHub.
  image: https://opengraph.githubassets.com/7eac57546a326d086c654dacea350cbc72eda1aa2e0abebc3485f4b912571c90/yu-yuxuan/HexGen_Hex2Spline
  title: GitHub - yu-yuxuan/HexGen_Hex2Spline
  url: https://github.com/yu-yuxuan/HexGen_Hex2Spline
- description: Jessica Zhang - Mechanical Engineering
  image: https://engineering.cmu.edu/_files/images/socialmedia/default.jpg
  title: Jessica Zhang
  url: https://www.meche.engineering.cmu.edu/directory/bios/zhang-yongjie.html
- description: ''
  image: ''
  title: URL Shortener, Branded Short Links & Analytics | TinyURL
  url: https://tinyurl.com/ydnqewkz
original_url: https://t.me/MagicDPD/2001
source: tg
title: 'HexGen и Hex2Spline: ALLHEX и IGA сетки для LS-DYNA'
---

Коллеги, на мой взгляд, сегодня просто огненный контент. Представляю вам два открытых набора консольных утилит, HexGen и Hex2Spline, разработанные группой профессора Юнцзе Джессики Чжан (Yongjie Jessica Zhang) в Университете Карнеги-Меллон (Carnegie Mellon University). Что бы лучше понимать, эта группа очень тесно связана со всем, что сейчас делается в области IGA для LS-DYNA и Corefrom. 







Рассматриваемый комплект утилит позволяет на основе произвольной геометрии строить ALL-HEX неструктурированную сетку при помощи реализации алгоритма поликуба - это делает HexGen. А уже на основе полученной сетки Hex2Spline строить модель для IGA расчета, извлекая данные сплайнов Безье и записывая их в формат BEXT, напрямую читаемый LS-DYNA и визуализируемый в LS-PrePost. 







Что особенно приятно, так это степень проработки вопроса. В репозитории проекта вы найдете не только все сходные коды утилит и собранные бинарники по Windows - вы найдете подробные инструкции по пересборке утилит. Естественно, в репозитории есть и тренировочные примеры с итогами правильной работы софта. А еще есть сопроводительная научная статья, в которой вы найдете подробные инструкции как пользоваться всеми утилитами и как настраивать их работу для разных геометрических моделей.



Научная статья: https://arxiv.org/abs/2011.14213



Репозиторий проекта: https://github.com/yu-yuxuan/HexGen_Hex2Spline



Страничка группы профессора Джессики Чжан в Университете Карнеги-Меллон:  https://www.meche.engineering.cmu.edu/directory/bios/zhang-yongjie.html

#all-hex #ansys #bext #iga #ls-dyna #ls-prepost #open_source #polycube
https://tinyurl.com/ydnqewkz
by GlukRazor
