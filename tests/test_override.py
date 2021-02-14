import pytest

from jrnl.override import apply_overrides, _recursively_apply, _get_config_node


@pytest.fixture()
def minimal_config():
    cfg = {
        "colors": {"body": "red", "date": "green"},
        "default": "/tmp/journal.jrnl",
        "editor": "vim",
        "journals": {"default": "/tmp/journals/journal.jrnl"},
    }
    yield cfg


def test_apply_override(minimal_config):
    overrides = [{"editor": "nano"}]
    apply_overrides(overrides, minimal_config)
    assert minimal_config["editor"] == "nano"


def test_override_dot_notation(minimal_config):
    cfg = minimal_config.copy()
    overrides = [{"colors.body": "blue"}]
    cfg = apply_overrides(overrides=overrides, base_config=cfg)
    assert cfg["colors"] == {"body": "blue", "date": "green"}


def test_multiple_overrides(minimal_config):
    overrides = [
        {"colors.title": "magenta"},
        {"editor": "nano"},
        {"journals.burner": "/tmp/journals/burner.jrnl"},
    ]  # as returned by parse_args, saved in parser.config_override

    cfg = apply_overrides(overrides, minimal_config.copy())
    assert cfg["editor"] == "nano"
    assert cfg["colors"]["title"] == "magenta"
    assert "burner" in cfg["journals"]
    assert cfg["journals"]["burner"] == "/tmp/journals/burner.jrnl"


def test_recursively_apply():
    cfg = {"colors": {"body": "red", "title": "green"}}
    cfg = _recursively_apply(cfg, ["colors", "body"], "blue")
    assert cfg["colors"]["body"] == "blue"


def test_get_config_node(minimal_config):
    assert len(minimal_config.keys()) == 4
    assert _get_config_node(minimal_config, "editor") == "vim"
    assert _get_config_node(minimal_config, "display_format") == None


from jrnl.override import _get_key_and_value_from_pair


def test_get_kv_from_pair():
    pair = {"ab.cde": "fgh"}
    k, v = _get_key_and_value_from_pair(pair)
    assert k == "ab.cde"
    assert v == "fgh"


from jrnl.override import _convert_dots_to_list


class TestDotNotationToList:
    def test_unpack_dots_to_list(self):

        keys = "a.b.c.d.e.f"
        keys_list = _convert_dots_to_list(keys)
        assert len(keys_list) == 6

    def test_sequential_delimiters(self):
        k = "g.r..h.v"
        k_l = _convert_dots_to_list(k)
        assert len(k_l) == 4
