# outofcloud_test


Тестовое задание от Out of Cloud

Реализовать граббер статей с новостных сайтов:

http://lenta.ru/rss 

http://www.interfax.ru/rss.asp

http://www.kommersant.ru/RSS/news.xml

http://www.m24.ru/rss.xml


Базовый функционал:

*  Получение списка свежих статей из rss-канала заданного источника.
   Каждый элемент данного списка представляет собой ссылку, заголовок, краткое описание, дату публикации.
*  Получение содержимого статьи по ссылке заданного источника.
   Результат должен содержать заголовок статьи, содержимое статьи в виде списка абзацев с чистым текстом (без html), ссылку на изображение, которое ассоциируется со      статьей (если такая имеется в источнике).


Запуск

Склонируйте репозиторий и выполните:

- python3.7 -m venv venv
- source venv/bin/activate
- установите зависимости: pip install -r requirements



### Пример работы для lenta.ru

```python
  from rss_parser import Grabber                                                                                                                                                                      

  gr = Grabber()                                                                                                                                                                                      

  data = gr.lenta.news(limit=3)   
  
  data                                                                                                                                                                                                
 [{'title': 'Стало известно о массовом выезде россиян в соседнюю европейскую страну',
  'link': 'https://lenta.ru/news/2020/11/11/fin/',
  'desc': 'Более 50 тысяч человек пересекли российско-финскую границу в октябре. Эти показатели оказались самыми высокими за последние полгода — начиная с апреля, когда ограничения, введенные из-за пандемии коронавируса, заработали в полную силу. В сентябре пересечений границы было на 2,3 тысячи меньше.',
  'published': '11.11.2020 14:04',
  'image': 'https://icdn.lenta.ru/images/2020/11/11/15/20201111155953665/pic_8fbb3ce7b6bec2e1448727d2f531891c.jpg'},
 {'title': 'Под Петербургом муж выстрелил жене в лицо и зарубил ее в торговом центре',
  'link': 'https://lenta.ru/news/2020/11/11/piter/',
  'desc': 'Под Санкт-Петербургом в салон красоты ворвался вооруженный пистолетом и топором мужчина, он убил 36-летнюю сотрудницу прямо на рабочем месте. Нападавший дважды выстрелил женщине в лицо, а затем зарубил топором. Она скончалась от полученных травм на месте преступления. Убийца оказался мужем погибшей.',
  'published': '11.11.2020 14:02',
  'image': 'https://icdn.lenta.ru/images/2020/11/11/16/20201111161457882/pic_a900ba2fbc138eec01355dc10e97aed3.jpg'},
 {'title': 'Назван переломный момент для российской экономики',
  'link': 'https://lenta.ru/news/2020/11/11/moment/',
  'desc': 'Переломный момент наступит для российской экономики в феврале-марте следующего года. Об этом заявил вице-премьер Андрей Белоусов. Он также отметил, что коронавирус отбросил Россию на 1,5 года назад, многие отрасли пострадали. Белоусов надеется, что экономику ждет смена вектора с негативного на позитивный в феврале.',
  'published': '11.11.2020 13:58',
  'image': 'https://icdn.lenta.ru/images/2020/11/11/16/20201111160916274/pic_39d1826d010690e5a78dd551db8ec801.jpg'}]
  
  link = data[0]['link']                                                                                                                                                                              

  link                                                                                                                                                                                                
  'https://lenta.ru/news/2020/11/11/fin/'

  full_data = gr.lenta.grub(link)                                                                                                                                                                     

  full_data                                                                                                                                                                                           

  [{'title': 'Стало известно о массовом выезде россиян в соседнюю европейскую страну',  
  'content': ['Более 50 тысяч человек пересекли российско-финскую границу в октябре. О массовом выезде россиян в соседнюю страну стало известноинтернет-газете «Фонтанка».',
   'По данным издания, эти показатели оказались самыми высокими за последние полгода — начиная с апреля, когда ограничения, введенные из-за пандемии коронавируса, заработали в полную силу. При этом в сентябре пересечений границы было на 2,3 тысячи меньше.',
   'Финские пограничники, к которым журналисты обратились за комментарием, отметили, что причины поездок россиян им неизвестны. «Статистика не отслеживает цель поездки, и поэтому точного ответа на вопрос о причине роста числа российских пассажиров нет. Вполне возможно, что одной из причин являются собственники недвижимости», — отметили в Пограничной службе Финляндии.',
   'Финляндия ввела ограничения на границе с Россией в условиях пандемии коронавируса 19 марта. С 1 октября страна разрешила въезд владельцам дач. Как отмечает издание, это и могло привести к резкому росту потока пассажиров.',
   'Ранее сообщалось, что финские власти в очередной разотказалисьоткрывать внешние границы для приезжих из России. О том, на какой период продлен запрет, не уточняется.',
   'С начала пандемии в Финляндии было зафиксировано 18,1 тысячи случаев заражения коронавирусом. 12,7 тысячи человек выздоровели, 363 скончались от осложнений, вызванных заболеванием.'],
  'image': 'https://icdn.lenta.ru/images/2020/11/11/15/20201111155953665/pic_8fbb3ce7b6bec2e1448727d2f531891c.jpg'}]

```
