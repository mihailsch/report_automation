import os
import pandas as pd
from datetime import datetime

# Автоматически определяем путь к input_docs
current_dir = os.path.dirname(os.path.abspath(__file__))  # директория, где работаем
input_path = os.path.join(current_dir, 'input_docs')

# Создаем папку если ее нет
os.makedirs(input_path, exist_ok=True)

# Загружаем таблицы в переменную
paths = {}

for tab in ['control.xls', 'storage1_main.xlsx', 'storage2_ip.xlsx']:
    file_path = os.path.join(input_path, tab)
    paths[tab] = file_path

try:
    control = pd.read_excel(paths.get('control.xls'))
    storage1_main = pd.read_excel(paths.get('storage1_main.xlsx'))
    storage2_ip = pd.read_excel(paths.get('storage2_ip.xlsx'))
except FileNotFoundError as e:
    print(f'File_read_error: Файл не найден: {e}')
    print('Проверьте, что в папке "input_path" есть файлы: control.xls, storage1_main.xlsx, storage2_ip.xlsx')
    print('Требуемая структура файлов: "item_name", "quantity"')

except Exception as e:
    print(f'File_read_error: Ошибка при чтении файлов: {e}')
    print('Возможные причины: поврежденные файлы, неверный формат, нет прав доступа')

dfs = {
    'control' : control,
    'storage1_main' : storage1_main,
    'storage2_ip' : storage2_ip
}

for name, df in dfs.items():
    df['quantity'] = df['quantity'].fillna(0)

for name, df in dfs.items():
    dfs[name] = df.rename(columns={'quantity' : f'{name}_quantity'})

control = dfs.get('control')
storage1_main = dfs.get('storage1_main')
storage2_ip = dfs.get('storage2_ip')


merged_pre = pd.merge(storage1_main,
                      control,
                      how='outer',
                      on='item_name')

merged = pd.merge(merged_pre,
                  storage2_ip,
                  how='outer',
                  on='item_name')

merged = merged.fillna(0)

def shuffle(row):
    # В функцию передается строка датафрейма
    # Задача скорректировать количество товара на storage1_main_quantity с учтом storage2_ip_quantity, а именно чтобы разница между main и control
    # нивелировалась с помощью ip
    # Функция работает по следующей логике:
    # если кол-во товара storage1_main_quantity < control_quantity, но при этом storage2_ip_quantity > 0
    # тогда на склад storage1_main_quantity перемещаем столько товара, чтобы control_quantity = storage1_main_quantity
    # иначе возвращаем исходное значение
    upd_row = row.copy()
    if upd_row['storage1_main_quantity'] < upd_row['control_quantity'] and upd_row['storage2_ip_quantity'] > 0:
        diff = upd_row['control_quantity'] - upd_row['storage1_main_quantity']
        if upd_row['storage2_ip_quantity'] <= diff:
            result = upd_row['storage1_main_quantity'] + upd_row['storage2_ip_quantity']
            return result
        elif upd_row['storage2_ip_quantity'] > diff:
            result = upd_row['storage2_ip_quantity'] + diff
            return result
    else: 
        return upd_row['storage1_main_quantity']
    

merged['corrected_main_quantity'] = merged.apply(shuffle, axis=1)
merged['control_except_main'] = merged['control_quantity'] - merged['corrected_main_quantity']

positive_result = merged[merged['control_except_main'] > 0]
negative_result = merged[merged['control_except_main'] < 0]

positive_result_final = positive_result[['item_name', 'control_except_main']]

positive_result_final = (
    positive_result_final
        .rename(columns={'control_except_main' : 'positive_result'})
        .sort_values('item_name', ascending=True)
)

negative_result_final = negative_result[['item_name', 'control_except_main']]

negative_result_final = (
    negative_result_final
        .rename(columns={'control_except_main' : 'negative_result'})
        .sort_values('item_name', ascending=True)
)

def save_reports(report1_df=positive_result_final, 
                 report2_df=negative_result_final, 
                 current_dir=current_dir):
    #Функция сохраняет датафреймы в папку output_docs
    
    # Путь к папке output_docs (относительно скрипта)
    output_dir = os.path.join(current_dir, "output_docs")
    
    # Создаем папку если ее нет
    os.makedirs(output_dir, exist_ok=True)
    
    # Генерируем имена файлов с временной меткой
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Пути к файлам
    file1_path = os.path.join(output_dir, f"1_positive_result_{timestamp}.xlsx")
    file2_path = os.path.join(output_dir, f"2_negative_result_{timestamp}.xlsx")
    
    # Сохраняем в Excel
    report1_df.to_excel(file1_path, index=False)
    report2_df.to_excel(file2_path, index=False)
    
    print(f"✓ Отчеты сохранены в папку: {output_dir}")
    print(f"  Report 1: {os.path.basename(file1_path)}")
    print(f"  Report 2: {os.path.basename(file2_path)}")
    
    return file1_path, file2_path

save_reports()

print('Скрипт завершил работу, нажмите Enter...')
input()