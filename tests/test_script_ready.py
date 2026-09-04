from scripts.script_ready import notific


def test_script_ready():
    res = notific()
    assert res == "Среда готова"
