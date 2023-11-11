from core.core import AspxParser

regExp = r'<mso:(.*?)\s+msdt:dt="string">(.*?)<\/mso:\1>'
path_to_files = ".../files/**/*.aspx"

parser = AspxParser(path_to_files,'-', regExp)
parser.save_data("output.json")