# from products.categories_list import *

# # Для категории
# for i in range(len(first_categories)):
#     category = first_categories[i]['category']
#     Category.objects.create(name=category)
# # Для подкатегории
# for i in range(len(first_categories)):
#     product = first_categories[i]['products']
#     category = first_categories[i]['category']
#     for j in product:
#         subcategory = j['title']
#         category_id = Category.objects.get(name=category)
#         SubCategory.objects.create(name=subcategory, category_id=category_id)
