from html import unescape
from bs4 import BeautifulSoup
import re
import json
import os
from glob import glob
from accessify import private, protected

# Путь к вашим файлам ASPX
path_to_files = "C:/Developments/python/aspx-parser/files/**/*.aspx"

class AspxParser:
	def __init__(self, path_to_files, json_fields, regExp):
		self.path_to_files = path_to_files
		self.json_fields = json_fields
		self.regExp = regExp
		self.js_data = []
		self.regExp = regExp
		self.get_files_list()
		self.parse_files()
        
    # список файлов в текущем каталоге с расширением ASPX
	def get_files_list(self):        
		self.files = glob(self.path_to_files, recursive=True)
		return self.files

	def parse_files(self):

		for file_name in self.files:
			file_path = os.path.join(path_to_files, file_name)

			with open(file_path, 'r', encoding='utf-8') as file:
				content = file.read()

				json_data = {}
		
				soup = BeautifulSoup(content, 'html.parser')
				title_tag = soup.title
				title_text = title_tag.text if title_tag else ''
				json_data['title'] = title_text

				# Перебираем каждое mso поле в CustomDocumentProperties
				mso_fields = re.findall(self.regExp, content, re.DOTALL)
			
				for field in mso_fields:
					field_name = field[0]
					field_content = field[1]
		
					# Разэкранирование HTML сущностей
					unescaped_content = unescape(field_content)
     
					soup = BeautifulSoup(unescaped_content, "html.parser")
     
					clean_content = str(soup)

					json_data[field_name] = clean_content

				filtered_data = {
					"title": json_data.get("title", ""),
					"description": json_data.get("CanvasContent1", ""),
					"imgUrl": json_data.get("BannerImageUrl", ""),
					"author": json_data.get("display_urn_x003a_schemas-microsoft-com_x003a_office_x003a_office_x0023__AuthorByline", ""),
					"publishedDate": json_data.get("FirstPublishedDate", "")
				}

				self.js_data.append(filtered_data)
    
	def get_data(self):
		return self.js_data

	# Сохраняем данные в файл JSON
	def save_data(self, path):		
		
		output_file_path = path
		with open(output_file_path, 'w', encoding='utf-8') as json_file:
			json.dump(self.js_data, json_file, ensure_ascii=False, indent=4)



