from core.core import AspxParser
regExp = r'<mso:(.*?)\s+msdt:dt="string">(.*?)<\/mso:\1>'

parser = AspxParser("C:/Developments/python/aspx-parser/files/**/*.aspx",'-', regExp)
parser.save_data("output.json")