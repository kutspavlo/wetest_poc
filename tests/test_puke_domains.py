import pytest
import requests
from enums.prod_domains import ProductionDomains


@pytest.mark.domains
@pytest.mark.parametrize("domain_url", [
    ProductionDomains.MAIN_PRIMARY,
    ProductionDomains.MAIN_SECONDARY,
    ProductionDomains.BACKUP_PRIMARY,
    ProductionDomains.BACKUP_SECONDARY

])
def test_puke_production_domains(record_property, domain_url, production_domain_snapshot):
    record_property("domain_url", domain_url.value)

    response = requests.get(domain_url.value)

    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"

    response_data = response.json()
    record_property("status_code", response.status_code)
    record_property("response_body", response_data)
    actual_proxies = response_data["config"]["proxies"]
    expected_proxies = production_domain_snapshot["config"]["proxies"]

    for key, expected_value in expected_proxies.items():
        actual_value = actual_proxies.get(key)

        assert actual_value == expected_value, \
            f"Value mismatch for '{key}'. Expected: {expected_value}, Got: {actual_value}"
