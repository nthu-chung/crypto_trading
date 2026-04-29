from cyqnt_trd.strategy_cases import (
    list_case_ids,
    load_case,
    load_case_preset,
    load_case_readme,
    load_catalog,
)


def test_strategy_case_catalog_contains_curated_cases():
    catalog = load_catalog()
    case_ids = list_case_ids()

    assert catalog["version"] == 1
    assert case_ids == [
        "rsi-mean-reversion",
        "btc-multi-factor-trend",
        "bb-squeeze-momentum",
        "quadruple-filter-breakout",
        "structure-breakout-priceaction",
    ]


def test_each_packaged_case_bundle_is_loadable():
    for case_id in list_case_ids():
        case = load_case(case_id)
        preset = load_case_preset(case_id)
        readme = load_case_readme(case_id)

        assert case["case_id"] == case_id
        assert preset["case_id"] == case_id
        assert isinstance(readme, str)
        assert len(readme) > 20
