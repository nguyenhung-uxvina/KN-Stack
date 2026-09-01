from leo_bridge import templates


def test_templates_path_resolves_to_existing_file():
    # In whatever layout this runs (canonical or flattened plugin), the
    # module-level TEMPLATES_PATH must point at a file that actually exists.
    assert templates.TEMPLATES_PATH.exists(), templates.TEMPLATES_PATH


def test_load_templates_returns_all_expected_modes():
    loaded = templates.load_templates()
    for mode in templates.EXPECTED_MODES:
        assert mode in loaded, f"missing mode {mode}"
