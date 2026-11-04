import requests 
response = requests.get("https://open.er-api.com/v6/latest/USD") 
if response.status_code == 200: 
 du_lieu = response.json() 
 ty_gia_vnd = du_lieu["rates"]["VND"] 
 print(f"1 USD = {ty_gia_vnd:,.0f} VND") 
else: 
 print("Khong lay duoc ty gia, ma loi:", response.status_code) 
