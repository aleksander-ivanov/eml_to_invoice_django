import io
import logging
import zipfile

import mailparser

from main.modules.eml_parser.eml_parser import EmlParser
from main.modules.invoice_date_extractor import invoice_date_extractor
from main.modules.pdf_builder.pdf_builder import PdfBuilder

logger = logging.getLogger(__name__)


class Zipper:

    @staticmethod
    def build_zip(req_file, company, user, invoice_number) -> bytes:
        try:
            mail = mailparser.parse_from_bytes(req_file.file.getvalue())
            invoice_date, due_date = invoice_date_extractor.extract(req_file.name)
            invoices = EmlParser.parse(mail.body, invoice_number)

            docs = PdfBuilder.build(invoices, company, user, invoice_date, due_date)

            return Zipper._zip_files(docs)

        except Exception as e:
            logger.error(e)

    @staticmethod
    def _zip_files(docs) -> bytes:
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as zipF:
            for invoice_name, bt in docs.items():
                zipF.writestr(invoice_name, bt)

        buffer.seek(0)
        return buffer.getvalue()