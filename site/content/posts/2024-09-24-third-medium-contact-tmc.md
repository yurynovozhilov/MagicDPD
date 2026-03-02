---
date: 2024-09-24 12:02:00+00:00
link_previews:
- description: ''
  image: ''
  title: Third medium contact method - Wikiwand
  url: https://www.wikiwand.com/en/articles/Third_medium_contact_method
- description: "\U0001D403\U0001D422\U0001D41D \U0001D432\U0001D428\U0001D42E \U0001D424\U0001D427\U0001D428\U0001D430
    \U0001D42D\U0001D421\U0001D41A\U0001D42D \U0001D413\U0001D421\U0001D422\U0001D42B\U0001D41D
    \U0001D40C\U0001D41E\U0001D41D\U0001D422\U0001D42E\U0001D426 \U0001D402\U0001D428\U0001D427\U0001D42D\U0001D41A\U0001D41C\U0001D42D
    \U0001D41C\U0001D41A\U0001D427 \U0001D421\U0001D41A\U0001D427\U0001D41D\U0001D425\U0001D41E
    \U0001D42C\U0001D421\U0001D41A\U0001D42B\U0001D429 \U0001D41E\U0001D41D\U0001D420\U0001D41E\U0001D42C?\n\nThe
    Half-height C-shape has become the benchmark problem for TMC models. Below is
    a comparison between a conventional contact solution (blue) and a TMC solution
    (magenta) using HuHu regularization.\n\nTMC is a simple contact method where the
    solids are embedded in an extremely compliant medium that stiffens and thus transfers
    forces when compressed towards zero volume. In the animation, the third medium
    is the meshed"
  image: https://dms.licdn.com/playlist/vid/v2/D4D05AQFVvTsvjqanZQ/thumbnail-with-play-button-overlay-high/B4DZnGSV3eIgBA-/0/1759968321217?e=2147483647&v=beta&t=43AJO4RCfgMJeeEhJEK0vJy6pHgln62no0eY_aoXKPQ
  title: '#topologyoptimization | Andreas Henrik Frederiksen | 13 comments'
  url: https://www.linkedin.com/posts/andreas-henrik-frederiksen_topologyoptimization-ugcPost-7237259131554811905-bkC5/
original_url: https://t.me/MagicDPD/2786
source: tg
title: Third Medium Contact (TMC)
---

В последнее время мне регулярно попадаются посты про моделирование контактного взаимодействия на основе метода третьей среды или Third Medium Contact (TMC). И вот что я вычитал про данный подход.

Итак, во более менее популярных коммерческих прочностных кодах реализованы контактны алгоритмы (здесь и далее я говорю про нелинейные контакты с рением и разделением) на основе штрафных функций в разных вариациях, множителей Лагранжа или нормального метод Лагранжа.

Если же посмотреть на TMC, то для меня он выглядит как вывернутый штрафной подход. Если в штрафном подходе контакт реализуется за счет штрафных сил, зависящих от глубины проникновения, то в TMC, за контакт отвечает сжатие это несчастной третьей среды. Получается, что у нас "пружинки" на примере которых обычно описывают работу контактов, торчат наружу. Кажется, в русскоязычной литературе это называется внешней барьерной функцией. Только тут эти пружинки еще и нелинейные, так как они состоят не одного элемента, а из нескольких элементов, содержащий материал третьей среды.

Выглядит все достаточно сложно, особенно конда визуализируют деформацию третьей среды. А что ты думаете?
https://www.wikiwand.com/en/articles/Third_medium_contact_method
https://www.linkedin.com/posts/andreas-henrik-frederiksen_topologyoptimization-ugcPost-7237259131554811905-bkC5/
