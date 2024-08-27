from django.utils.safestring import mark_safe


class CustomFormMixin:
    def as_div(self):
        return self._html_output(
            normal_row='<div class="form-group mb-3"><div class="mb-1 text-body-default">%(label)s</div> %(errors)s %(field)s %(help_text)s</div>',
            error_row='<div class="alert alert-danger">%s</div>',
            row_ender='</div>',
            help_text_html='<small class="form-text text-muted">%s</small>',
            errors_on_separate_row=False
        )
        
    def _html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        rows = []
        
        non_field_errors = self.non_field_errors()

        if non_field_errors:
            rows.append(f'<div class="alert alert-danger mb-3">{"<br>".join(non_field_errors)}</div>')
        
        for field in self:
            errors = ''.join([f'<div class="alert alert-danger mb-1">{e}</div>' for e in field.errors])
            row = normal_row % {
                'label': field.label_tag(),
                'errors': errors,
                'field': field,
                'help_text': field.help_text,
            }
            rows.append(row)
        return mark_safe(''.join(rows))