import random

def random_menu():
    random_list = ["แกงผักหวานไข่มดแดง", "แกงอ่อม", "แกงหน่อไม้", "ต้มส้มปลานิล", "แกงเห็ด", "ต้มแซ่บกระดูกอ่อน"]
    menu_data = random.choice(random_list)
    
    print(menu_data)
    
random_menu()