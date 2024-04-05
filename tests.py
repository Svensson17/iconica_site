import pytest
from base_script import TemplateFiller
from fixtures.datasets.data_list import data_list
from fixtures.datasets.template_paths import template_paths
from fixtures.datasets.template_order import template_order
from fixtures.datasets.output_paths import output_paths


@pytest.fixture
def template_filler():
    return TemplateFiller(template_paths, output_paths, data_list, template_order)


def test_validate_templates(capsys, template_filler):
    template_filler = TemplateFiller(template_paths, output_paths, data_list, template_order)
    template_filler.validate_templates()
    captured_out, _ = capsys.readouterr()
    assert "Ошибка в шаблоне" not in captured_out


def test_fill_templates(template_filler):
    template_filler.fill_templates()
