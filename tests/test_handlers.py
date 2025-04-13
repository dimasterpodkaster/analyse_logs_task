import pytest
from reports.handlers import HandlersReport


@pytest.mark.parametrize("data, total_expected", [
    (
        [{"/api/v1/orders/": {"INFO": 2}, "/api/v1/payments/": {"ERROR": 1}}],
        3
    ),
    (
        [{"/api/v1/orders/": {"INFO": 1}}, {"/api/v1/auth/": {"INFO": 2, "WARNING": 1}}],
        4
    ),
])
def test_handlers_total_requests(data, total_expected):
    report = HandlersReport()
    output = report.generate(data)
    assert f"Total requests: {total_expected}" in output


@pytest.mark.parametrize("data, path_expected", [
    (
        [{"/api/v1/orders/": {"INFO": 2}, "/api/v1/payments/": {"ERROR": 1}}],
        "/api/v1/payments/"
    ),
    (
        [{"/api/v1/orders/": {"INFO": 1}}, {"/api/v1/auth/": {"INFO": 2, "WARNING": 1}}],
        "/api/v1/orders/"
    ),
])
def test_handlers_report_generation(data, path_expected):
    report = HandlersReport()
    output = report.generate(data)

    assert path_expected in output


@pytest.mark.parametrize("input_data, expected_order", [
    (
        [
            {"/api/v1/orders/": {"INFO": 1}, "/admin/": {"INFO": 2}, "/api/v1/payments/": {"INFO": 1}},
        ],
        ["/admin/", "/api/v1/orders/", "/api/v1/payments/"]
    ),
    (
        [
            {"/api/v1/checkout/": {"INFO": 1}, "/admin/dashboard/": {"INFO": 2}},
        ],
        ["/admin/dashboard/", "/api/v1/checkout/"]
    )
])
def test_handlers_report_sort_order(input_data, expected_order):
    report = HandlersReport()
    output = report.generate(input_data)

    lines = output.splitlines()
    handler_lines = [line.strip() for line in lines if line.startswith("/")]
    actual_order = [line.split()[0] for line in handler_lines]

    assert actual_order == expected_order
