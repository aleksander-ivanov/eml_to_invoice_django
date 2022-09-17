from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle
import numpy as np
import io

from main.models import Company
from users.models import AppUser


class PdfBuilder:

    @staticmethod
    def build(invoices: dict, company: Company, user: AppUser, invoice_date, due_date) -> dict:

        result = {}
        for k, v in invoices.items():
            from_to_data = [
                [],
                ["From", "To"],
                [user.get_full_name(), company.name],
                [user.address, company.address],
                [user.country, company.country],
                [user.email, company.email],
                [user.phone, ""],
                [],
                [f"Invoice No.: {k}", ""],
                [f"Invoice Date: {invoice_date.strftime('%b %d, %Y')}",
                 f"Due: {due_date.strftime('%b %d, %Y')}"],
                []
            ]

            currency = v.iloc[0][-1]
            v = v.iloc[:, :-1]
            total = v[v.columns[-1]].sum()

            v[v.columns[1:]] = v[v.columns[1:]].applymap(lambda x: f'{x:.2f}')
            v.iloc[:, -1] = v.iloc[:, -1].apply(lambda x: f'{currency} {x}')
            items_data = np.insert(v.to_numpy(), 0, v.columns, 0).tolist()

            summary_data = [
                ["Invoice Summary"],
                ["Subtotal", f"{currency} {total:.2f}"],
                ["Total", f"{currency} {total:.2f}"]
            ]

            filename = f'Invoice {k}.pdf'
            buffer = io.BytesIO()
            docu = SimpleDocTemplate(buffer, title=filename, rightMargin=0.5 * inch)

            styles = getSampleStyleSheet()
            doc_style = styles["Definition"]
            doc_style.alignment = 1

            title = Paragraph("INVOICE", doc_style)

            items_style = TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
                ('LINEABOVE', (0, 0), (-1, -1), 0.25, colors.black),
                ('LINEBELOW', (0, -1), (-1, -1), 0.25, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),  # TODO: Test Total column
                ('ALIGN', (0, 0), (0, -1), 'LEFT')
            ])

            summary_style = TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
                ('LINEABOVE', (0, 0), (-1, -1), 0.25, colors.black),
                ('LINEBELOW', (0, -1), (-1, -1), 0.25, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
            ])

            from_to_style = TableStyle([
                ("TEXTCOLOR", (0, 1), (-1, 1), colors.grey),
                ('ALIGN', (1, 1), (-1, -1), 'LEFT')
            ])

            # creates a table object using the Table() to pass the table data and the style object
            items_table = Table(items_data, style=items_style,
                                colWidths=[4 * inch, 1 * inch, 1 * inch, 1 * inch], hAlign='RIGHT',
                                rowHeights=0.5 * inch)

            summary_table = Table(summary_data, style=summary_style,
                                  colWidths=[1.5 * inch, 1.5 * inch], hAlign='RIGHT',
                                  rowHeights=0.5 * inch)

            from_to_table = Table(from_to_data, style=from_to_style,
                                  colWidths=[3 * inch, 3 * inch])

            # finally, we have to build the actual pdf merging all objects together
            doc_parts = [title, from_to_table, items_table, summary_table]
            docu.build(doc_parts)
            buffer.seek(0)

            result[filename] = buffer.getvalue()

        return result
