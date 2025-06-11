import streamlit as st
import pandas as pd

# Настройка стилей страницы
st.set_page_config(
    page_title="Анализатор инцидентов нефтегазовой отрасли",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS стили
st.markdown("""
    <style>
    /* Основные стили */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Заголовок */
    .header {
        color: #1E3F66;
        padding-bottom: 20px;
    }
    
    /* Контейнеры */
    .stContainer {
        background-color: #F0F8FF;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 5px solid #1E3F66;
    }
    
    /* Кнопки */
    .stButton>button {
        background-color: #1E3F66;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 24px;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #2A4D7A;
        color: white;
    }
    
    /* Поля ввода */
    .stNumberInput>div>div>input, .stTextInput>div>div>input {
        border: 1px solid #1E3F66;
    }
    
    /* Мультивыбор */
    .stMultiSelect>div>div>div>div {
        border: 1px solid #1E3F66;
    }
    
    /* Предупреждения */
    .stAlert {
        border-left: 5px solid #FFA500;
    }
    
    /* Таблицы */
    .dataframe {
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Графики */
    [data-testid="stArrowVegaLiteChart"] {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Подсказки */
    .stTooltip {
        background-color: #1E3F66 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Заголовок приложения
st.markdown("<h1 class='header' style='text-align: center;'>Анализатор инцидентов нефтегазовой отрасли</h1>", unsafe_allow_html=True)

# Загрузка данных
dataset = pd.read_csv('database.csv')
# Формируем список тегов с указанием типов данных
available_tegs = [f"{col} ({dataset[col].dtype})" for col in dataset.columns]

# Основной контент
with st.container():
    st.markdown("<div class='stContainer'>", unsafe_allow_html=True)
    
    # Поле выбора тегов (столбцов) с типами данных
    select_tegs_with_types = st.multiselect('Выберите теги: ', available_tegs, 
                                          help="Выберите столбцы для анализа")
    
    # Получаем только имена столбцов без типов для дальнейшей обработки
    select_tegs = [col.split(' (')[0] for col in select_tegs_with_types]
    
    st.markdown("</div>", unsafe_allow_html=True)

# Контейнеры для управления данными
with st.container():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("<div class='stContainer'>", unsafe_allow_html=True)
        range_ds = st.number_input("Сколько строк датасета необходимо вывести: ", 
                                 min_value=0, max_value=len(dataset),
                                 help="Введите 0, чтобы использовать диапазон")
        st.write("ИЛИ")
        
        col1_1, col2_1 = st.columns([1, 1])
        with col1_1:
            diap1 = st.number_input("С какой строки начать: ", 
                                 min_value=0, max_value=len(dataset),
                                 value=0)
        with col2_1:
            diap2 = st.number_input("До какой строки закончить: ", 
                                 min_value=diap1, max_value=len(dataset),
                                 value=min(100, len(dataset)))
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"<div class='stContainer' style='height: 100%; display: flex; align-items: center; justify-content: center;'>"
                   f"<div style='text-align: center;'>"
                   f"<h4>Всего строк в датасете:</h4>"
                   f"<h2>{len(dataset)}</h2>"
                   f"</div></div>", 
                   unsafe_allow_html=True)

# Кнопки действий
col_btn1, col_btn2, col_btn3 = st.columns(3)
with col_btn1:
    show_data = st.button('Показать данные', key='show_data')
with col_btn2:
    show_hist = st.button('Построить гистограмму', key='show_hist')
with col_btn3:
    show_stats = st.button('Рассчитать статистику', key='show_stats')

# Обработка кнопки "Показать данные"
if show_data:
    st.markdown("<div class='stContainer'>", unsafe_allow_html=True)
    st.subheader("Результаты")
    
    if not select_tegs:  # Если не выбраны теги/столбцы
        if range_ds != 0:  # Если задан range_ds (вывод первых N строк)
            st.dataframe(dataset.head(range_ds))
        else:  # Если range_ds = 0, используем диапазон diap1-diap2
            st.dataframe(dataset.iloc[diap1:diap2 + 1])  # iloc для индексации
    else:  # Если выбраны теги/столбцы
        if range_ds != 0:  # Вывод первых N строк выбранных столбцов
            st.dataframe(dataset[select_tegs].head(range_ds))
        else:  # Вывод диапазона diap1-diap2 для выбранных столбцов
            st.dataframe(dataset[select_tegs].iloc[diap1:diap2 + 1])
    
    st.markdown("</div>", unsafe_allow_html=True)

# Обработка кнопки "Построить гистограмму"
if show_hist:
    st.markdown("<div class='stContainer'>", unsafe_allow_html=True)
    st.subheader("Гистограммы")
    
    if not select_tegs:  # Если не выбраны столбцы
        st.warning("Пожалуйста, выберите хотя бы один столбец!")
    else:
        numeric_columns = []
        for col in select_tegs:
            if pd.api.types.is_numeric_dtype(dataset[col]):
                numeric_columns.append(col)
        
        if not numeric_columns:  # Если нет числовых столбцов
            st.warning("Выбранные столбцы не содержат числовых данных для построения гистограммы!")
        else:
            # Строим гистограммы только для числовых столбцов
            for col in numeric_columns:
                if range_ds != 0:
                    st.subheader(f"Гистограмма для '{col}'")
                    st.bar_chart(dataset[col].head(range_ds))
                else:
                    st.subheader(f"Гистограмма для '{col}'")
                    st.bar_chart(dataset[col].iloc[diap1:diap2 + 1])
    
    st.markdown("</div>", unsafe_allow_html=True)

# Обработка кнопки "Рассчитать статистические характеристики"
if show_stats:
    st.markdown("<div class='stContainer'>", unsafe_allow_html=True)
    st.subheader("Статистический анализ")
    
    if not select_tegs:  # Если не выбраны столбцы
        st.warning("Пожалуйста, выберите хотя бы один столбец!")
    else:
        numeric_columns = []
        for col in select_tegs:
            if pd.api.types.is_numeric_dtype(dataset[col]):
                numeric_columns.append(col)
        
        if not numeric_columns:  # Если нет числовых столбцов
            st.warning("Выбранные столбцы не содержат числовых данных для анализа!")
        else:
            # Определяем данные для анализа (весь датасет или выбранный диапазон)
            if range_ds != 0:
                data_to_analyze = dataset.head(range_ds)
            else:
                data_to_analyze = dataset.iloc[diap1:diap2 + 1]
            
            # Создаем DataFrame для статистики
            stats_df = pd.DataFrame(index=[
                "Количество значений", 
                "Среднее значение", 
                "Стандартное отклонение", 
                "Минимальное значение", 
                "25-й перцентиль", 
                "Медиана", 
                "75-й перцентиль", 
                "Максимальное значение"
            ])
            
            # Заполняем статистику для каждого числового столбца
            for col in numeric_columns:
                col_data = data_to_analyze[col]
                stats_df[col] = [
                    col_data.count(),
                    col_data.mean(),
                    col_data.std(),
                    col_data.min(),
                    col_data.quantile(0.25),
                    col_data.median(),
                    col_data.quantile(0.75),
                    col_data.max()
                ]
            
            # Отображаем таблицу с округленными значениями
            try:
                import matplotlib
                st.dataframe(stats_df.style.background_gradient(cmap='Blues'))
            except ImportError:
                st.dataframe(stats_df.round(2))  # Простое отображение без стилизации
                st.warning("Для цветового оформления таблицы установите matplotlib: `pip install matplotlib`")
            
            # Дополнительная информация
            st.markdown("""
            **Пояснение показателей:**
            - **Количество значений**: Число непустых значений в столбце
            - **Среднее значение**: Среднее арифметическое всех значений
            - **Стандартное отклонение**: Мера разброса данных
            - **Перцентили**: Значения, ниже которых находится определенный процент данных
            - **Медиана**: Значение, разделяющее данные пополам (50-й перцентиль)
            """)
    
    st.markdown("</div>", unsafe_allow_html=True)

   
    
    
    
    
    
    
    
    
    
    
    
    
    
    