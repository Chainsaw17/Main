#Создание СППР с помощью streamlit

import streamlit as st  #Streamlit — это фреймворк для языка программирования Python
import streamlit as st  #Streamlit — это фреймворк для языка программирования Python
import pandas as pd   #для вывода таблиц (в виде dataframe)
import numpy as np
import matplotlib.pyplot as plt  #для графика
from streamlit_modal import Modal
import streamlit.components.v1 as components

with st.sidebar: #боковая панель с кнопками задач для отображения информации без загромождения основной области контента веб-приложений 
    st.title("Калькулятор калорий")
    sex = st.radio(
        "Ваш пол:",
        ["Мужской", "Женский"])
    
    #числовое поле ввода для количества видов ценных бумаг в портфеле
    age = st.number_input("Введите ваш возраст:",
                            min_value = 0,
                            max_value = 100,
                            value = 20,
                            step = 1)

    #числовое поле ввода для ожидаемой доходности портфеля
    height = st.number_input("Введите ваш рост в сантиментрах:",
                            min_value = 1,
                            value = 180,
                            step = 1)

    weight = st.number_input("Введите ваш вес в килограммах:",
                            min_value = 1,
                            value = 80,
                            step = 1)

    style = st.radio(
        "Ваша дневная активность:",
        options=[
            "Очень низкая. Редко выхожу из дома, почти не гуляю",
            "Низкая. Хожу в магазин или недолго прогуливаюсь",
            "Средняя. Занимаюсь активными видами спорта 2-3 раза в неделю",
            "Высокая. Занимаюсь активными видами спорта 3-5 раза в неделю",
            "Очень высокая. Занимаюсь активным спортом не менее 5 раз в неделю"
        ])
    goal = st.select_slider(
        "Ваша цель:",
        value = "Поддерживать вес",
        options=[
            "Снизить вес",
            "Поддерживать вес",
            "Набрать вес"
        ])
    
    if sex == "Мужской":
        BMR = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
    else:
        BMR = 44.76 + (9.2 * weight) + (3.1 * height) - (4.3 * age)

    if style == "Низкая. Хожу в магазин или недолго прогуливаюсь":
        BMR *= 1.2
    elif style == "Средняя. Занимаюсь активными видами спорта 2-3 раза в неделю":
        BMR *= 1.55
    elif style == "Высокая. Занимаюсь активными видами спорта 3-5 раза в неделю":
        BMR *= 1.725
    elif style == "Очень высокая. Занимаюсь активным спортом не менее 5 раз в неделю":
        BMR *= 1.9

    if goal == "Снизить вес":
        BMR *= 0.9
    elif goal == "Набрать вес":
        BMR *= 1.1

    BMR = round(BMR)
    if goal == "Снизить вес":
        protein = BMR * 0.45 / 4
        fat = BMR * 0.35 / 9
        carbo = BMR * 0.15 / 4
    elif goal == "Набрать вес":
        protein = BMR * 0.3 / 4
        fat = BMR * 0.2 / 9
        carbo = BMR * 0.5 / 4
    else:
        protein = BMR * 0.3 / 4
        fat = BMR * 0.3 / 9
        carbo = BMR * 0.4 / 4
        
    protein = round(protein)
    fat = round(fat)
    carbo = round(carbo)
    

st.title(f"В день вам необходимо потреблять {BMR} ккал")
st.write(f"Из них: {protein} г. белков, {fat} г. жиров, {carbo} г. углеводов.")
st.info('Хотите контролировать свой вес? Рассчитайте свой рацион!')

if 'result_df' not in st.session_state:
    st.session_state['result_df'] = pd.DataFrame(columns=[
        'Продукт',
        'Вес',
        'Белки, г',
        'Жиры, г',
        'Углеводы, г',
        'Калорийность, ккал'
        ])
if 'result_df_rec' not in st.session_state:
    st.session_state['result_df_rec'] = pd.DataFrame(columns=[
        'Продукт',
        'Вес',
        'Белки, г',
        'Жиры, г',
        'Углеводы, г',
        'Калорийность, ккал'
        ])
if 'с' not in st.session_state:
    st.session_state['c'] = pd.DataFrame(columns=[
        'Продукт',
        'Вес',
        'Белки, г',
        'Жиры, г',
        'Углеводы, г',
        'Калорийность, ккал'
        ])
if 'd' not in st.session_state:
    st.session_state['d'] = pd.DataFrame(columns=[
        'Продукт',
        'Вес',
        'Белки, г',
        'Жиры, г',
        'Углеводы, г',
        'Калорийность, ккал'
        ])

data_df = pd.read_excel("kkal.xlsx") #, delimiter = ';')
data_df=data_df.fillna(0)
data_df['str'] = 'В 100 гр. продукта(кбжу): ' + data_df['Калорийность, ккал'].astype(str) + ', ' + data_df['Белки, г'].astype(str) + ', ' + data_df['Жиры, г'].astype(str) + ', ' + data_df['Углеводы, г'].astype(str)
#data_df_edit = st.data_editor(data_df)

text_search = st.text_input("Введите искомый продукт и нажмите Enter:",
                            value="")
if text_search != '':
    data_search = data_df[data_df["Продукт"].str.contains(text_search)]
    product = st.radio(
    "Возможно, вы имели ввиду это:",
    data_search["Продукт"],
    captions = data_search['str'],
    index = None,
    )
    weight = st.number_input("Введите вес в граммах",
                             step = 1,
                             min_value = 1)
    button1 = st.button('Добавить')
    if button1:
        b = data_df[data_df["Продукт"]==product]
        b['Вес']=weight
        b['Белки, г'] = b['Белки, г'] * weight / 100
        b['Жиры, г'] = b['Жиры, г'] * weight / 100
        b['Углеводы, г'] = b['Углеводы, г'] * weight / 100
        b['Калорийность, ккал'] = b['Калорийность, ккал'] * weight / 100
        b = b.drop(columns=['str'])
    else:
        b = pd.DataFrame()
else:
    b = pd.DataFrame()


st.write('Не нашли что искали? Добавьте продукт сами!')
modal = Modal(
    "Добавить продукт:",
    key="demo-modal",
    padding=10,  # по умолчанию
    max_width=500  # по умолчанию
)
open_modal = st.button("Добавить продукт")
if open_modal:
    modal.open()
    

if modal.is_open():
    with modal.container():
        prod_name = st.text_input('Название продукта')
        prod_kkal = st.number_input("Калорийность на 100 г.",
                             step = 1,
                             min_value = 1)
        prod_prot = st.number_input("Белки на 100 г., г",
                             step = 1,
                             min_value = 1)
        prod_fat = st.number_input("Жиры на 100 г., г",
                             step = 1,
                             min_value = 1)
        prod_carb = st.number_input("Углеводы на 100 г., г",
                             step = 1,
                             min_value = 1)
        prod_weight = st.number_input("Вес, г",
                             step = 1,
                             min_value = 1)
        prod_button = st.button('Готово')
        if prod_button:
            st.session_state.c = pd.DataFrame({'Продукт': [prod_name],
                       'Вес': [prod_weight],
                       'Белки, г': [prod_prot*prod_weight/100],
                       'Жиры, г': [prod_fat*prod_weight/100],
                       'Углеводы, г': [prod_carb*prod_weight/100],
                       'Калорийность, ккал': [prod_kkal*prod_weight/100]})
            st.session_state.result_df = pd.concat([st.session_state.result_df, st.session_state.c],
                                       ignore_index=True)
            modal.close()

st.write('Или добавьте свой рецепт!')
modal2 = Modal(
    "Добавить рецепт:",
    key="modal2",
    padding=10,  # по умолчанию
    max_width=500  # по умолчанию
)
open_modal2 = st.button("Добавить рецепт")
if open_modal2:
    modal2.open()
    st.session_state.result_df_rec = pd.DataFrame(columns=[
        'Продукт',
        'Вес',
        'Белки, г',
        'Жиры, г',
        'Углеводы, г',
        'Калорийность, ккал'
        ])
    

if modal2.is_open():
    with modal2.container():
        rec_name = st.text_input('Название рецепта')
        text_search_rec = st.text_input("Введите искомый ингредиент:",
                            value="")
        if text_search_rec != '':
            data_search_rec = data_df[data_df["Продукт"].str.contains(text_search_rec)]
            product_rec = st.radio(
            "Возможно, вы имели ввиду этот ингредиент:",
            data_search_rec["Продукт"],
            captions = data_search_rec['str'],
            index = None,
            )
            weight_ing = st.number_input("Введите вес ингредиента в граммах",
                                     step = 1,
                                     min_value = 1)
            button_ing = st.button('Добавить ингредиент')
            if button_ing:
                b_rec = data_df[data_df["Продукт"]==product_rec]
                b_rec['Вес'] = weight_ing
                b_rec['Белки, г'] = b_rec['Белки, г'] * weight_ing / 100
                b_rec['Жиры, г'] = b_rec['Жиры, г'] * weight_ing / 100
                b_rec['Углеводы, г'] = b_rec['Углеводы, г'] * weight_ing / 100
                b_rec['Калорийность, ккал'] = b_rec['Калорийность, ккал'] * weight_ing / 100
                b_rec = b_rec.drop(columns=['str'])
            else:
                b_rec = pd.DataFrame()
        else:
            b_rec = pd.DataFrame()
        st.session_state.result_df_rec = pd.concat([st.session_state.result_df_rec, b_rec],
                                  ignore_index=True)
        result_df_rec_edit = st.dataframe(st.session_state.result_df_rec,
                              hide_index=True,
                              on_select="rerun",
                              selection_mode=["multi-row"])
        button2_rec = st.button('Удалить ингредиент')
        if button2_rec:
            st.session_state.result_df_rec.drop(result_df_rec_edit.selection['rows'],
                                            inplace = True)
            st.rerun()
        weight_rec = st.number_input("Введите вес порции блюда в граммах",
                                     step = 1,
                                     min_value = 1)
        rec_button = st.button('Блюдо готово')
        if rec_button:
            st.session_state.result_df_rec['Вес_Белки'] = st.session_state.result_df_rec['Вес'] * st.session_state.result_df_rec['Белки, г']
            prot_rec_mean = st.session_state.result_df_rec['Вес_Белки'].sum() / st.session_state.result_df_rec['Вес'].sum()
            st.session_state.result_df_rec['Вес_Жиры'] = st.session_state.result_df_rec['Вес'] * st.session_state.result_df_rec['Жиры, г']
            fat_rec_mean = st.session_state.result_df_rec['Вес_Жиры'].sum() / st.session_state.result_df_rec['Вес'].sum()
            st.session_state.result_df_rec['Вес_Углеводы'] = st.session_state.result_df_rec['Вес'] * st.session_state.result_df_rec['Углеводы, г']
            carg_rec_mean = st.session_state.result_df_rec['Вес_Углеводы'].sum() / st.session_state.result_df_rec['Вес'].sum()
            st.session_state.result_df_rec['Вес_Калорийность'] = st.session_state.result_df_rec['Вес'] * st.session_state.result_df_rec['Калорийность, ккал']
            kkal_rec_mean = st.session_state.result_df_rec['Вес_Калорийность'].sum() / st.session_state.result_df_rec['Вес'].sum()
            st.session_state.d = pd.DataFrame({'Продукт': [rec_name],
                       'Вес': [weight_rec],
                       'Белки, г': [prot_rec_mean*weight_rec/100],
                       'Жиры, г': [fat_rec_mean*weight_rec/100],
                       'Углеводы, г': [carg_rec_mean*weight_rec/100],
                       'Калорийность, ккал': [kkal_rec_mean*weight_rec/100]})
            st.session_state.result_df = pd.concat([st.session_state.result_df, st.session_state.d],
                                       ignore_index=True)
            modal2.close()
        



  
st.session_state.result_df = pd.concat([st.session_state.result_df, b],
                                       ignore_index=True)

result_df_edit = st.dataframe(st.session_state.result_df,
                              hide_index=True,
                              on_select="rerun",
                              selection_mode=["multi-row"])

st.write('Ввели не тот продукт? Просто выделите ненужную строчку и нажмите "Удалить"')
button2 = st.button('Удалить')
if button2:
    st.session_state.result_df.drop(result_df_edit.selection['rows'],
                                    inplace = True)
    st.rerun()

kkal_sum = st.session_state.result_df['Калорийность, ккал'].sum()
if kkal_sum/BMR<=1:
    kkal_all = st.progress(value=kkal_sum/BMR,
                           text=f'Калории: {kkal_sum} ккал из {BMR} ккал')
else:
    kkal_all = st.progress(value=1.0,
                           text=f'Калории: {kkal_sum} ккал из {BMR} ккал')

protein_sum = st.session_state.result_df['Белки, г'].sum()
if protein_sum/protein<=1:
    protein_all = st.progress(value=protein_sum/protein,
                              text=f'Белки: {protein_sum} г. из {protein} г.')
else:
    protein_all = st.progress(value=1.0,
                              text=f'Белки: {protein_sum} г. из {protein} г.')

fat_sum = st.session_state.result_df['Жиры, г'].sum()
if fat_sum/fat<=1:
    fat_all = st.progress(value=fat_sum/fat,
                          text=f'Жиры: {fat_sum} г. из {fat} г.')
else:
    fat_all = st.progress(value=1.0,
                          text=f'Жиры: {fat_sum} г. из {fat} г.')

carbo_sum = st.session_state.result_df['Углеводы, г'].sum()
if carbo_sum/carbo<=1:
    carbo_all = st.progress(value=carbo_sum/carbo,
                            text=f'Углеводы: {carbo_sum} г. из {carbo} г.')
else:
    carbo_all = st.progress(value=1.0,
                            text=f'Углеводы: {carbo_sum} г. из {carbo} г.')





