import requests

response = requests.get("https://gitlab.com/api/v4/users/techworld-with-nana/projects")
print(f"\nqueried API at endpoint \nhttps://gitlab.com/api/v4/users/techworld-with-nana/projects")

cnt = 1
print(f" ___________________________________________________________\n" \
      f"|                                                           |\n"\
      f"|    user techworld-with-nana has {len(response.json())} public projects         |")
for project in response.json():
  print(f"|    {cnt}:")
  print(f"|     name: {project['name']}")
  print(f"|     last_active: {project['last_activity_at']}")
  cnt += 1
print(f"|                                                           |\n"\
      f"|___________________________________________________________|")

posts = requests.get("https://jsonplaceholder.typicode.com/posts").json()
print(f"\n\nqueried API at endpoint \nhttps://jsonplaceholder.typicode.com/posts")
user_word_count = {}
min_title_length = 9999
min_title_user = 0
for post in posts:
  title_length = len(post["title"].split(" "))
  if title_length < min_title_length:
    min_title_length = title_length
    min_title_user = post["userId"]
  word_count = len(post["body"].split(" "))
  if post["userId"] not in user_word_count:
    user_word_count[post["userId"]] = word_count
  else:
    user_word_count[post["userId"]] += word_count

max_body_count = 0
max_body_user = 0
for user in user_word_count.items():
  if max_body_count < user[1]:
    max_body_count = user[1]
    max_body_user = user[0]


print(f" ___________________________________________________________\n" \
      f"|                                                           |\n"\
      f"|    user id with shortest title: {min_title_user}         \n"\
      f"|    title length: {min_title_length}                           \n"\
      f"|                                                           |\n"\
      f"|    user id with highest word count: {max_body_user}         \n"\
      f"|    word count: {max_body_count}                           \n"\
      f"|___________________________________________________________|")