#for autowritten slugfield
def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya', 
         ' ': '-', '_': '-', '-': '-'}

    return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))


# from categories_list import *
# from models import Category, SubCategory

# from products.models import *

# from products.categories_list import first_categories

# for cat in first_categories:
#     new_cat = Category(name=cat['category'])
#     new_cat.save()
#     for subcat in cat['products']:
#         new_subcat = SubCategory(name=subcat['title'], category_id=new_cat)
#         new_subcat.save()