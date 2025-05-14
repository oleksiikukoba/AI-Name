import streamlit as st
from openai import OpenAI

# НОВИЙ детальний промпт
SEO_PROMPT_TEMPLATE = """Ти — ШІ-агент, який спеціалізується на SEO-оптимізації контенту. Твоє завдання — автоматично перетворити опис відео в якісний, зрозумілий та добре оптимізований для пошукових систем текст. Виконуй завдання, дотримуючись наступних інструкцій:

1.  **Визначення ключових слів:** Визнач головні ключові слова та фрази, які максимально відповідають тематиці відео.
2.  **Використання ключових слів:** Використовуй ключові слова природно і логічно по всьому тексту, уникаючи перенасичення (keyword stuffing).
3.  **Структура тексту:**
    * Розбий текст на чіткі, логічні абзаци.
    * Використовуй заголовки (наприклад, H2, H3) для структурування.
    * Створи текст у форматі: короткий вступ, розгорнута основна частина, висновок.
    * Використовуй марковані та нумеровані списки, якщо це доречно для полегшення читання та представлення інформації.
4.  **Обсяг тексту:** Дотримуйся рекомендованого обсягу основного SEO-тексту в межах 200–400 слів.
5.  **Мета-теги:**
    * Згенеруй унікальний, привабливий **Мета-заголовок** (до 60 символів). Він повинен містити основні ключові слова.
    * Згенеруй інформативний **Мета-опис** (до 160 символів). Він також повинен містити основні ключові слова та спонукати до перегляду.
6.  **Формат виведення:** Надай відповідь чітко розділяючи основний SEO-текст, Мета-заголовок та Мета-опис. Наприклад:

    **Мета-заголовок:**
    [Тут мета-заголовок]

    **Мета-опис:**
    [Тут мета-опис]

    **SEO-оптимізований текст:**
    [Тут основний SEO-текст згідно інструкцій]

Ось опис відео для перетворення:
{video_description_placeholder}

Створи SEO-оптимізований текст, Мета-заголовок та Мета-опис, суворо дотримуючись вказаних вимог.
"""

# Ініціалізація OpenAI клієнта
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e: # Більш загальний виняток, оскільки st.secrets може викликати різні помилки
    st.error(f"Помилка завантаження OpenAI API ключа: {e}. Переконайтесь, що файл .streamlit/secrets.toml існує та містить правильний ключ OPENAI_API_KEY.")
    st.stop() # Зупинити виконання, якщо ключ не завантажено

def generate_seo_text(original_description: str) -> str:
    """
    Генерує SEO-оптимізований текст, мета-заголовок та мета-опис за допомогою OpenAI API.
    """
    if not original_description.strip():
        return "Будь ласка, введіть оригінальний опис відео."

    full_prompt = SEO_PROMPT_TEMPLATE.replace("{video_description_placeholder}", original_description)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Або іншу модель, наприклад, gpt-4o-mini або gpt-4o, якщо доступна і бажана
            messages=[
                {"role": "system", "content": "Ти — ШІ-агент, який спеціалізується на SEO-оптимізації контенту."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7, # Можна налаштувати для більшої/меншої креативності
            max_tokens=2000  # Збільшив max_tokens, щоб вмістити текст + метадані
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Сталася помилка під час звернення до OpenAI API: {e}"

# Streamlit UI
st.set_page_config(page_title="Army TV Оптимізатор Тексту", layout="wide")

st.title("🤖 ArmyTV. Лейтенант ШІ оптимізує для тебе")
st.markdown("""
Я допоможу тобі перетворити звичайний опис на інформативний та структурований текст, який буде краще
індексуватися пошуковими системами. Я також згенерую мета-заголовок та мета-опис.
""")

st.header("📝 Вхідні дані")
original_text = st.text_area("Вставте сюди оригінальний опис вашого відео:", height=200, key="original_text_input")

if 'seo_text' not in st.session_state:
    st.session_state.seo_text = ""

if st.button("🚀 Оптимізувати текст!", type="primary", use_container_width=True):
    if original_text:
        with st.spinner("✨ Магія ArmyTV... Лейтенант ШІ працює над оптимізацією. Будь ласка, зачекайте."):
            st.session_state.seo_text = generate_seo_text(original_text)
    else:
        st.warning("Будь ласка, введіть текст для оптимізації.")

if st.session_state.seo_text:
    st.header("💡 Лейтенант ШІ оптимізував текст (та додав мета-теги)")
    st.text_area("Результат (включно з мета-заголовком та мета-описом):", value=st.session_state.seo_text, height=600, key="seo_text_output", help="Ви можете скопіювати цей текст. Перевірте наявність Мета-заголовку та Мета-опису на початку.")
    # Кнопка для копіювання (потребує встановлення streamlit-extras, або можна обійтись без неї)
    # from streamlit_extras.keyboard_text import key_to_text # Потребує pip install streamlit-extras
    # st.code(st.session_state.seo_text) # Альтернативний спосіб показати для копіювання
    # if st.button("Копіювати текст"):
    #     st.components.v1.html(f"<script>navigator.clipboard.writeText({json.dumps(st.session_state.seo_text)});</script><div>Скопійовано!</div>", height=50)

st.markdown("""
---
*Побудовано з ❤️ для ArmyTV.*
""")