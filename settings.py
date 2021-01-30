import os

# Server data
base_url = 'https://petfriends1.herokuapp.com/'

# User login valid data
valid_email = 'ebonhawk@bk.ru'
valid_password = 'qwert6657Y'

# User login invalid data
invalid_email = 'invalid_email_313@bk.ru'
invalid_password = 'invalid_password_313'
invalid_api_key = 'invalid_api_key_313'

# Pets settings
pet1photo = os.path.join("..", "mmedia", "Barsic.jpg")
pet2photo = os.path.join("..", "mmedia", "Bobik.jpg")
pet3photo = os.path.join("..", "mmedia", "Sonic.jpg")
text_photo = os.path.join("..", "mmedia", "testfile.txt")
invalid_photo = os.path.join("..", "mmedia", "badphoto.jpg")
long_name = 'a ' * 130 + 'b'
