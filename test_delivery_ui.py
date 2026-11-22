import pytest
from playwright.sync_api import expect


@pytest.mark.parametrize("amount, zone, fee, total", [
    pytest.param(0, "city", 1000, 1000, id="TC01"),
    pytest.param(9999, "city", 1000, 10999, id="TC02"),
    pytest.param(10000, "city", 0, 10000, id="TC03"),
    pytest.param(10001, "city", 0, 10001, id="TC04"),
    pytest.param(0, "region", 2000, 2000, id="TC05"),
    pytest.param(9999, "region", 2000, 11999, id="TC06"),
    pytest.param(10000, "region", 0, 10000, id="TC07"),
    pytest.param(10001, "region", 0, 10001, id="TC08"),
])
def test_delivery(page, amount, zone, fee, total):
    page.get_by_label("Сумма заказа").fill(str(amount))
    page.get_by_label("Зона доставки").select_option(zone)
    page.get_by_role("button", name="Рассчитать").click()
    result = page.get_by_role("status")
    expect(result).to_be_visible()
    expect(result).to_have_text(
        f"Доставка: {fee} ₸. К оплате: {total} ₸."
    )
    expect(page.get_by_role("alert")).to_be_hidden()


@pytest.mark.parametrize("amount", [
    pytest.param("", id="TC09"),
    pytest.param("-1", id="TC10"),
    pytest.param("12.5", id="TC11"),
])
def test_invalid_amount(page, amount):
    page.get_by_label("Сумма заказа").fill(amount)
    page.get_by_role("button", name="Рассчитать").click()
    error = page.get_by_role("alert")
    expect(error).to_be_visible()
    expect(error).to_have_text(
        "Введите целое неотрицательное число"
    )
    expect(page.get_by_role("status")).to_be_hidden()


@pytest.mark.parametrize("zone", [pytest.param("region", id="TC12")])
def test_reset(page, zone):
    amount = page.get_by_label("Сумма заказа")
    area = page.get_by_label("Зона доставки")
    result = page.get_by_role("status")
    error = page.get_by_role("alert")

    amount.fill("5000")
    area.select_option(zone)
    page.get_by_role("button", name="Рассчитать").click()
    expect(result).to_be_visible()
    expect(result).to_have_text("Доставка: 2000 ₸. К оплате: 7000 ₸.")

    page.get_by_role("button", name="Сбросить").click()
    expect(amount).to_have_value("")
    expect(area).to_have_value("city")
    expect(error).to_be_hidden()
    expect(result).to_be_hidden()
