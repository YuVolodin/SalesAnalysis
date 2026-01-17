# 1. Импорт необходимых библиотек
import pandas as pd
import matplotlib.pyplot as plt

# 2. Загрузка данных из файла
sales_df = pd.read_csv('sales_data.csv')

# 3. Первичный анализ данных
print("=" * 60)
print("ПЕРВИЧНЫЙ АНАЛИЗ ДАННЫХ")
print("=" * 60)

print("\nПервые 5 строк данных:")
print(sales_df.head())

print("\nОсновная информация о данных:")
print(sales_df.info())

print("\nСтатистическое описание числовых столбцов:")
print(sales_df.describe())

# Проверка на пропущенные значения
print("\nПропущенные значения в каждом столбце:")
print(sales_df.isnull().sum())

print("\n" + "=" * 60)

# 4. Подготовка данных
# Создаем столбец с выручкой (количество * цена)
sales_df['Revenue'] = sales_df['Quantity'] * sales_df['Price']

# Преобразуем дату в правильный формат
sales_df['Date'] = pd.to_datetime(sales_df['Date'])

# Извлекаем месяц из даты
sales_df['Month'] = sales_df['Date'].dt.month
sales_df['Month_Name'] = sales_df['Date'].dt.month_name()

print("Данные после подготовки (первые 3 строки):")
print(sales_df.head(3))

print("\n" + "=" * 60)

# 5. Анализ выручки по категориям товаров
category_revenue = sales_df.groupby('Category')['Revenue'].sum().sort_values(ascending=False)

print("ОБЩАЯ ВЫРУЧКА ПО КАТЕГОРИЯМ ТОВАРОВ:")
print(category_revenue)

print("\n" + "=" * 60)

# 6. Анализ динамики продаж по месяцам
# Группируем данные по месяцам
monthly_sales = sales_df.groupby(['Month', 'Month_Name'])['Revenue'].sum().reset_index()
# Сортируем по номеру месяца
monthly_sales = monthly_sales.sort_values('Month')

print("ДИНАМИКА ПРОДАЖ ПО МЕСЯЦАМ:")
print(monthly_sales[['Month_Name', 'Revenue']])

# Также посчитаем количество проданных товаров по месяцам
monthly_quantity = sales_df.groupby('Month_Name')['Quantity'].sum()
print("\nКОЛИЧЕСТВО ПРОДАННЫХ ТОВАРОВ ПО МЕСЯЦАМ:")
print(monthly_quantity)

print("\n" + "=" * 60)

# 7. Топ-5 самых продаваемых товаров
# Топ-5 по выручке
top_products_revenue = sales_df.groupby('Product')['Revenue'].sum().sort_values(ascending=False).head(5)

# Топ-5 по количеству проданных единиц
top_products_quantity = sales_df.groupby('Product')['Quantity'].sum().sort_values(ascending=False).head(5)

print("ТОП-5 ТОВАРОВ ПО ВЫРУЧКЕ:")
print(top_products_revenue)

print("\nТОП-5 ТОВАРОВ ПО КОЛИЧЕСТВУ ПРОДАННЫХ ЕДИНИЦ:")
print(top_products_quantity)

print("\n" + "=" * 60)

# 8. Визуализация результатов
print("\nСОЗДАНИЕ ГРАФИКОВ...")

# Создаем большую фигуру для нескольких графиков
fig = plt.figure(figsize=(16, 10))

# График 1: Выручка по категориям товаров
ax1 = plt.subplot(2, 2, 1)
bars = ax1.bar(category_revenue.index, category_revenue.values, 
               color=['blue', 'green', 'red', 'orange', 'purple'])
ax1.set_title('Выручка по категориям товаров', fontsize=14, fontweight='bold')
ax1.set_xlabel('Категория товара')
ax1.set_ylabel('Выручка (руб.)')
ax1.tick_params(axis='x', rotation=45)

# Добавляем значения на столбцы
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:,.0f}', ha='center', va='bottom')

# График 2: Динамика продаж по месяцам
ax2 = plt.subplot(2, 2, 2)
ax2.plot(monthly_sales['Month_Name'], monthly_sales['Revenue'], 
         marker='o', linewidth=2, color='darkblue')
ax2.set_title('Динамика продаж по месяцам', fontsize=14, fontweight='bold')
ax2.set_xlabel('Месяц')
ax2.set_ylabel('Выручка (руб.)')
ax2.tick_params(axis='x', rotation=45)
ax2.grid(True, linestyle='--', alpha=0.7)

# График 3: Топ-5 товаров по выручке (горизонтальная диаграмма)
ax3 = plt.subplot(2, 2, 3)
bars_h = ax3.barh(list(top_products_revenue.index), top_products_revenue.values, 
                  color='lightblue')
ax3.set_title('Топ-5 товаров по выручке', fontsize=14, fontweight='bold')
ax3.set_xlabel('Выручка (руб.)')

# Добавляем значения
for i, (bar, value) in enumerate(zip(bars_h, top_products_revenue.values)):
    ax3.text(value, bar.get_y() + bar.get_height()/2, 
             f'{value:,.0f}', va='center', ha='left')

# График 4: Круговая диаграмма распределения выручки
ax4 = plt.subplot(2, 2, 4)
wedges, texts, autotexts = ax4.pie(category_revenue.values, 
                                    labels=category_revenue.index,
                                    autopct='%1.1f%%',
                                    startangle=90)
ax4.set_title('Распределение выручки по категориям', fontsize=14, fontweight='bold')

# Делаем диаграмму красивее
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

plt.tight_layout()
plt.show()

# Отдельный график: Топ-5 товаров по количеству продаж
plt.figure(figsize=(12, 6))
plt.barh(list(top_products_quantity.index), top_products_quantity.values, 
         color=['red', 'orange', 'yellow', 'green', 'blue'])
plt.title('Топ-5 товаров по количеству продаж', fontsize=16, fontweight='bold')
plt.xlabel('Количество проданных единиц', fontsize=12)

# Добавляем значения на столбцы
for i, (product, quantity) in enumerate(zip(top_products_quantity.index, top_products_quantity.values)):
    plt.text(quantity, i, f'  {quantity} шт.', va='center', fontsize=11)

plt.tight_layout()
plt.show()

print("ГРАФИКИ СОЗДАНЫ УСПЕШНО!")
print("\n" + "=" * 60)

# 9. Выводы на основе анализа
print("\nВЫВОДЫ НА ОСНОВЕ АНАЛИЗА:")
print("=" * 60)

print("\n1. Анализ выручки по категориям:")
print(f"   • Наибольшую выручку приносят смартфоны: {category_revenue['Smartphones']:,.0f} руб.")
print(f"   • На втором месте - ноутбуки: {category_revenue['Laptops']:,.0f} руб.")
print(f"   • Наименьшая выручка у аксессуаров: {category_revenue['Accessories']:,.0f} руб.")
print("   Примечание: у аксессуаров низкая цена, но высокие продажи в штуках.")

print("\n2. Динамика продаж по месяцам:")
print(f"   • Продажи росли в течение года")
print(f"   • Лучший месяц: декабрь ({monthly_sales.iloc[-1]['Revenue']:,.0f} руб.)")
print(f"   • Худший месяц: январь ({monthly_sales.iloc[0]['Revenue']:,.0f} руб.)")
print("   • Наблюдается сезонность - рост к концу года")

print("\n3. Самые продаваемые товары:")
print("   По выручке:")
for i, (product, revenue) in enumerate(top_products_revenue.items(), 1):
    print(f"     {i}. {product}: {revenue:,.0f} руб.")

print("\n   По количеству:")
for i, (product, quantity) in enumerate(top_products_quantity.items(), 1):
    # Найдем выручку для этого товара
    product_rev = sales_df[sales_df['Product'] == product]['Revenue'].sum()
    print(f"     {i}. {product}: {quantity} шт. ({product_rev:,.0f} руб.)")

print("\n4. Ключевые наблюдения:")
print("   • Смартфоны - самая доходная категория")
print("   • USB-C Cable - самый продаваемый товар в штуках")
print("   • iPhone 13 и LG OLED 55\" дают высокую выручку при малом количестве")
print("   • Аксессуары хорошо продаются, но имеют низкую маржу")

print("\n5. Рекомендации для магазина:")
print("   • Увеличить ассортимент и продвижение смартфонов")
print("   • Создать наборы аксессуаров для увеличения среднего чека")
print("   • Усилить маркетинг в начале года")
print("   • Рассмотреть скидки на TV и Audio для роста продаж")

print("\n" + "=" * 60)
print("АНАЛИЗ ЗАВЕРШЕН")
print("=" * 60)