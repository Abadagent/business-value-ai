def calculate_business_value(data: dict) -> dict:
    multipliers = {
        "Торговля": 2.5,
        "Услуги": 3.0,
        "Общепит": 2.0,
        "Производство": 4.0,
        "Онлайн-бизнес": 4.5,
    }

    monthly_profit = data["monthly_profit"]
    annual_profit = monthly_profit * 12

    multiplier = multipliers.get(data["industry"], 3.0)
    value = annual_profit * multiplier

    risks = []

    if data["revenue_confirmed"] == "Нет":
        value *= 0.70
        risks.append("Нет подтверждения выручки")
    elif data["revenue_confirmed"] == "Частично":
        value *= 0.85
        risks.append("Выручка подтверждена только частично")

    if data["largest_client"] > 40:
        value *= 0.80
        risks.append("Высокая зависимость от одного клиента")

    if data["business_age"] < 2:
        value *= 0.85
        risks.append("Бизнес работает менее 2 лет")

    low_value = int(value * 0.85)
    high_value = int(value * 1.15)

    seller_price = data["seller_price"]

    if annual_profit > 0:
        payback_years = round(seller_price / annual_profit, 1)
        payback = f"{payback_years} лет"
    else:
        payback = "Нет прибыли"

    recommended_price = int(low_value * 0.90)

    if seller_price > high_value:
        deal_status = "🔴 Цена завышена"
    elif seller_price < low_value:
        deal_status = "🟢 Выгодная сделка"
    else:
        deal_status = "🟡 Рыночная цена"

    overpay_low = seller_price - high_value
    overpay_high = seller_price - low_value

    return {
        "low_value": low_value,
        "high_value": high_value,
        "payback": payback,
        "risks": risks,
        "recommended_price": recommended_price,
        "deal_status": deal_status,
        "overpay_low": overpay_low,
        "overpay_high": overpay_high,
    }