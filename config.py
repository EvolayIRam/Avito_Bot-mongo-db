##################
###AVITO SETUP####
##################
key = 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir'  # key
search = ''  # Строка поиска на сайте
categoryId = 0  # in category.json
locationId = 621540  # in region.json
searchRadius = 10  # Радиус поиска (км)
priceMin = 1000  # Минимальная цена
priceMax = 1000000  # Максимальная цена
owner = 'private'  # or company
sort = 'date'  # or priceAsc or priceDesc
withImagesOnly = 'true'  # Только с фото or false
limit_page = 50  # Количество объявлений на странице. 50 максимум.
display = 'list'  # or service
#########################
####PARSER/BOT SETUP#####
#########################
cookie = 'YOUR COOKIE HERE'
token = 'YOUR TELEGRAM TOKEN HERE'  # Токен телеграмм-бота
chat_id = 'YOUR USER CHAT ID HERE'  # Chat-ID User
admin_chat_id = 'YOUR ADMIN CHAT ITHERE'  # Chat-ID Admin
###############################
######MongoDB Settings#########
###############################
mongo_string = 'mongodb://root:YOURPASSWORD@YOURIP:27017/?tls=true&tlsAllowInvalidCertificates=true'  # Chat-ID Admin
current_db_name = 'All'
collection_name = 'All'
