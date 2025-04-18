# import requests

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
#     "Referer": "https://www.tamildailycalendar.com/"
# }

# url = "https://www.tamildailycalendar.com/2025/13042025.jpg"
# res = requests.get(url, headers=headers)
# print(res.content)

def parse_date(datestr: dict):
    
    return str(int(datestr["date"]))+datestr["month"]+datestr["year"]

print(parse_date({"date":"13","month":"04","year":"2025"}))

print(f"{4:03}")