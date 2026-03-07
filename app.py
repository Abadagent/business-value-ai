import pandas as pd
import streamlit as st

from valuation_logic import calculate_business_value


st.set_page_config(
    page_title="Проверка цены бизнеса за 2 минуты",
    layout="centered"
)


def save_request(data: dict) -> None:
    df = pd.DataFrame([data])
    df.to_csv("requests_log.csv", mode="a", header=False, index=False)


def save_lead(contact: str) -> None:
    lead_df = pd.DataFrame([{"contact": contact.strip()}])
    lead_df.to_csv("leads.csv", mode="a", header=False, index=False)


st.title("Узнайте, завышена ли цена бизнеса, за 2 минуты")
st.markdown(
    """
    **Для инвесторов, покупателей и продавцов бизнеса.**

    Сервис показывает:
    - ориентировочную стоимость бизнеса
    - переплату или запас по цене
    - окупаемость сделки
    - ключевые риски
    - итоговый вердикт по сделке
    """
)

st.info("Сейчас доступна 1 бесплатная экспресс-оценка.")

st.markdown("### Введите параметры бизнеса")

industry = st.selectbox(
    "Отрасль",
    ["Торговля", "Услуги", "Общепит", "Производство", "Онлайн-бизнес"]
)

monthly_revenue = st.number_input(
    "Месячная выручка (₸)",
    min_value=0,
    value=10000000,
    step=100000
)

monthly_profit = st.number_input(
    "Месячная чистая прибыль (₸)",
    min_value=0,
    value=2000000,
    step=100000
)

seller_price = st.number_input(
    "Цена продавца (₸)",
    min_value=0,
    value=50000000,
    step=100000
)

business_age = st.slider(
    "Сколько лет бизнесу",
    min_value=0,
    max_value=20,
    value=2
)

largest_client = st.slider(
    "Доля крупнейшего клиента (%)",
    min_value=0,
    max_value=100,
    value=20
)

revenue_confirmed = st.selectbox(
    "Подтверждение выручки",
    ["Да", "Частично", "Нет"]
)

if st.button("Проверить цену бизнеса"):
    data = {
        "industry": industry,
        "monthly_revenue": monthly_revenue,
        "monthly_profit": monthly_profit,
        "seller_price": seller_price,
        "business_age": business_age,
        "largest_client": largest_client,
        "revenue_confirmed": revenue_confirmed,
    }

    save_request(data)
    result = calculate_business_value(data)

    st.markdown("---")
    st.subheader("Вердикт по сделке")

    if "🔴" in result["deal_status"]:
        st.error(result["deal_status"])
    elif "🟢" in result["deal_status"]:
        st.success(result["deal_status"])
    else:
        st.warning(result["deal_status"])

    st.metric(
        "Вероятная переплата / запас по цене",
        f"{result['overpay_low']:,} — {result['overpay_high']:,} ₸"
    )

    st.markdown("### Результат оценки")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Ориентировочная стоимость",
            f"{result['low_value']:,} — {result['high_value']:,} ₸"
        )
        st.metric("Окупаемость", result["payback"])
        st.metric("Цена продавца", f"{seller_price:,} ₸")

    with col2:
        st.metric(
            "Рекомендуемая цена покупки",
            f"{result['recommended_price']:,} ₸"
        )
        st.metric("Индекс сделки", result["deal_status"])
        st.metric("Месячная прибыль", f"{monthly_profit:,} ₸")

    st.markdown("### Ключевые риски")
    if result["risks"]:
        for risk in result["risks"]:
            st.write(f"- {risk}")
    else:
        st.write("- Существенных рисков не выявлено")

    st.markdown("---")
    st.markdown("## Хотите сохранить результат и получить доступ к следующим оценкам?")
    st.write("Оставьте WhatsApp или email для раннего доступа.")

    lead_contact = st.text_input(
        "WhatsApp или email",
        key="lead_contact_after_result"
    )

    if st.button("Получить доступ"):
        if lead_contact.strip():
            save_lead(lead_contact)
            st.success("Контакт сохранён. Мы свяжемся с вами.")
        else:
            st.warning("Введите WhatsApp или email")

st.markdown("---")
st.markdown(
    """
    **Важно:** это экспресс-оценка, а не официальный отчёт об оценке.  
    Методика основана на базовых мультипликаторах и риск-корректировках.
    """
)
