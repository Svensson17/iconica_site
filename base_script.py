from docxtpl import DocxTemplate
from docx import Document
import re
import sys
from fixtures.datasets.data_list import data_list
from fixtures.datasets.template_paths import template_paths
from fixtures.datasets.template_order import template_order
from fixtures.datasets.output_paths import output_paths


class TemplateFiller:

    def __init__(self, template_paths, output_paths, data_list, template_order):
        self.template_paths = template_paths
        self.output_paths = output_paths
        self.data_list = data_list
        self.template_order = template_order

    def validate_templates(self):
        for template_path, data in zip(self.template_paths, self.data_list):
            template = DocxTemplate(template_path)

            try:
                template.render(data)
            except Exception as e:
                print(f"Ошибка в шаблоне {template_path}: {e}", file=sys.stdout)
                exit(1)

            template_vars = set(re.findall(r'\{\{\s*(\w+)\s*\}\}', template.get_xml()))
            data_vars = set(data.keys())
            missing_vars = template_vars - data_vars
            if missing_vars:
                print(f"В шаблоне {template_path} отсутствуют переменные: {', '.join(missing_vars)}", file=sys.stdout)

    def fill_templates(self):
        self.validate_templates()

        main_doc = Document()
        sorted_templates = sorted(
            zip(self.template_paths, self.output_paths, self.data_list),
            key=lambda x: self.template_order[x[0]]
        )
        for template_path, output_path, data in sorted_templates:
            template = DocxTemplate(template_path)
            template.render(data)

            for element in template.element.body:
                main_doc.element.body.append(element)
        main_doc.save('final_doc/final_doc.docx')


if __name__ == "__main__":
    template_paths = template_paths
    output_paths = output_paths
    data_list = data_list
    template_order = template_order

    filler = TemplateFiller(template_paths, output_paths, data_list, template_order)
    filler.fill_templates()

    print("OK")
