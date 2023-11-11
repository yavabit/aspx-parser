from html import unescape
from bs4 import BeautifulSoup
import re
import json
import os
from glob import glob

# Путь к вашим файлам ASPX
path_to_files = "C:/Developments/python/aspx-parser/files/**/*.aspx"
js_data = []

# Получим список файлов в текущем каталоге с расширением ASPX
files = glob(path_to_files, recursive=True)

# Обойдем каждый файл
for file_name in files:
	file_path = os.path.join(path_to_files, file_name)
	# Открываем файл и читаем его содержимое
	with open(file_path, 'r', encoding='utf-8') as file:
		content = file.read()

		# Создаем объект JSON
		json_data = {}
  
  		# Добавим поле title
		soup = BeautifulSoup(content, 'html.parser')
		title_tag = soup.title
		title_text = title_tag.text if title_tag else ''
		json_data['title'] = title_text

		# Перебираем каждое mso поле в CustomDocumentProperties
		mso_fields = re.findall(r'<mso:(.*?)\s+msdt:dt="string">(.*?)<\/mso:\1>', content, re.DOTALL)
    
		for field in mso_fields:
			field_name = field[0]
			field_content = field[1]
   
            # Разэкранирование HTML сущностей
			unescaped_content = unescape(field_content)
            # Очистка от HTML тегов
			#clean_content = BeautifulSoup(unescaped_content, "html.parser").text.strip()
			soup = BeautifulSoup(unescaped_content, "html.parser")
			for tag in soup.find_all(True):
				if tag.name not in ['br', 'p', 'ul', 'li', 'a']:
					tag.unwrap()
			clean_content = str(soup)
            # Добавление в JSON
			json_data[field_name] = clean_content

		filtered_data = {
            "title": json_data.get("title", ""),
            "description": json_data.get("CanvasContent1", ""),
            "imgUrl": "" if "amrestcloud" in json_data.get("BannerImageUrl", "") else json_data.get("BannerImageUrl", "").split(',')[0],
            "author": json_data.get("display_urn_x003a_schemas-microsoft-com_x003a_office_x003a_office_x0023__AuthorByline", ""),
            "publishedDate": json_data.get("FirstPublishedDate", "")
        }

		js_data.append(filtered_data)

# Сохраняем данные в файл JSON
output_file_path = "output.json"

with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(js_data, json_file, ensure_ascii=False, indent=4)
