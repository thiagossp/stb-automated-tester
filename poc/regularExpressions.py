import re
teste = 'asd11:12:13asd'

pattern = re.compile("[0-9]{2}:{1}[0-9]{2}")

print(pattern.search(teste).group(0)) if pattern.search(teste) is not None else print("None")

