import pandas as pd
import streamlit as st

from valuation_logic import calculate_business_value


st.set_page_config(
    page_title="Проверка цены бизнеса",
    layout="centered"
)


def save_request(data: dict) -> None:
    df = pd.DataFrame([data])
    df.to_csv("requests_log.csv", mode="a", header=False, index=False)


def save_lead(contact: str) -> None:
    lead_df = pd.DataFrame([{"contact": contact.strip()}])
    lead_df.to_csv("leads.csv", mode="a", header=False, index=False)


st.title("Проверка цены бизнеса за 2 минуты")
st.write("Узнайте, завышена ли цена сделки.")

st.markdown(
    """
    - стоимость бизнеса  
    - переплата или запас по цене  
    - окупаемость сделки  
    """
)

st.info("1 экспресс-оценка сейчас доступна бесплатно.")

col1, col2 = st.columns(2)

with col1:
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
        "Месячная прибыль (₸)",
        min_value=0,
        value=2000000,
        step=100000
    )

with col2:
    seller_price = st.number_input(
        "Цена продавца (₸)",
        min_value=0,
        value=50000000,
        step=100000
    )

    business_age = st.slider(
        "Возраст бизнеса (лет)",
        min_value=0,
        max_value=20,
        value=2
    )

    largest_client = st.slider(
        "Крупнейший клиент (%)",
        min_value=0,
        max_value=100,
        value=20
    )

revenue_confirmed = st.selectbox(
    "Подтверждение выручки",
    ["Да", "Частично", "Нет"]
)

if st.button("Проверить цену"):
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
    st.subheader("Вердикт")

    if "🔴" in result["deal_status"]:
        st.error(
            f"{result['deal_status']} | "
            f"Вероятная переплата: {result['overpay_low']:,} — {result['overpay_high']:,} ₸"
        )
    elif "🟢" in result["deal_status"]:
        st.success(result["deal_status"])
    else:
        st.warning(result["deal_status"])

    r1, r2, r3 = st.columns(3)

    with r1:
        st.metric(
            "Стоимость",
            f"{result['low_value']:,} — {result['high_value']:,} ₸"
        )

    with r2:
        st.metric("Окупаемость", result["payback"])

    with r3:
        st.metric("Цена продавца", f"{seller_price:,} ₸")

    st.write("### Риски")
    if result["risks"]:
        for risk in result["risks"]:
            st.write(f"- {risk}")
    else:
        st.write("- Существенных рисков не выявлено")

    st.write(
        f"**Рекомендуемая цена покупки:** {result['recommended_price']:,} ₸"
    )

    st.markdown("---")
    st.write("**Хотите сохранить результат и получить доступ к следующим оценкам?**")
    lead_contact = st.text_input("WhatsApp или email", key="lead_contact_after_result")

    if st.button("Получить доступ"):
        if lead_contact.strip():
            save_lead(lead_contact)
            st.success("Контакт сохранён")
        else:
            st.warning("Введите WhatsApp или email")

st.caption("Это экспресс-оценка, а не официальный отчёт.")
