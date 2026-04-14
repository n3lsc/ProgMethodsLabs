import pytest
from unittest.mock import MagicMock, patch

from view import CurrencyApp


# ---------- ФИКСТУРА БЕЗ Tk ----------
@pytest.fixture
def app():
    model = MagicMock()

    app = CurrencyApp.__new__(CurrencyApp)  # не вызываем __init__
    app.model = model

    # мокаем tree
    app.tree = MagicMock()

    return app


def test_add_calls_model(app):
    app.model.add.return_value = MagicMock(color="red",
                                           currency_name_1="USD",
                                           currency_name_2="EUR",
                                           rate=0.92,
                                           date="2024.05.12")

    # имитируем вставку в таблицу
    app.tree.insert = MagicMock()

    # вызываем напрямую
    obj = app.model.add("red", "USD", "EUR", "0.92", "2024.05.12")

    app.tree.insert(
        "",
        "end",
        values=(obj.color, obj.currency_name_1, obj.currency_name_2, obj.rate,
                obj.date),
    )

    app.model.add.assert_called_once()
    app.tree.insert.assert_called_once()


def test_delete_calls_model(app):
    app.tree.selection.return_value = ["item1"]
    app.tree.index.return_value = 0

    app.delete_item()

    app.model.delete.assert_called_with(0)
    app.tree.delete.assert_called()


def test_delete_error_shows_messagebox(app):
    app.tree.selection.return_value = ["item1"]
    app.tree.index.return_value = 0

    app.model.delete.side_effect = Exception("Ошибка")

    with patch("tkinter.messagebox.showerror") as mock_msg:
        app.delete_item()

        mock_msg.assert_called_once()


def test_populate_table(app):
    obj = MagicMock(color="red",
                    currency_name_1="USD",
                    currency_name_2="EUR",
                    rate=0.92,
                    date="2024.05.12")

    app.model.data = [obj]

    app.tree.insert = MagicMock()

    app.populate_table()

    app.tree.insert.assert_called_once()
