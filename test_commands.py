import pytest

from model import CurrencyModel, ValidationError


def test_process_commands_add_rem_save(tmp_path):
    cmds = tmp_path / "commands.txt"
    out_file = tmp_path / "out.txt"

    cmds.write_text("ADD red; USD; EUR; 0.92; 2024.05.12\n"
                    "ADD blue; EUR; RUB; 96.3; 2024.05.12\n"
                    "REM rate < 1.0\n"
                    f"SAVE {out_file}\n")

    model = CurrencyModel()
    # pre-existing item that should remain (rate 89.7)
    model.add("green", "USD", "RUB", "89.7", "2024.05.13")

    model.process_commands(cmds)

    # red had rate 0.92 and should be removed by REM
    rates = [o.rate for o in model.data]
    assert 0.92 not in rates
    assert 96.3 in rates
    assert 89.7 in rates

    # saved file must exist and include remaining items
    content = out_file.read_text()
    assert "blue EUR RUB 96.3" in content
    assert "green USD RUB 89.7" in content


def test_process_commands_add_invalid_raises(tmp_path):
    cmds = tmp_path / "commands2.txt"
    cmds.write_text("ADD only; three; fields\n")

    model = CurrencyModel()

    with pytest.raises(ValidationError):
        model.process_commands(cmds)
