from bs4 import BeautifulSoup

with open('moodletest.html', 'r') as f:
    html_doc = f.read()

soup = BeautifulSoup(html_doc, 'lxml')
course_list = soup.find_all('div', {'class': 'ml-1'})
arr = []
for i in course_list:
    for j in i.strings:
        arr.append(j)

print(arr)
print()
arr = list(filter(lambda a: a != "\n", arr))

for i in arr:
    print(i)
