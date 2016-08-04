import uuid
from html import escape

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'))

from parser_app.models import News, Category


class PDFGenerator():
    """Defines PDF-related infrastructure for news digest,
    contains external method for pdf generating. Relies on reportlab

    Usage:
    pdfgen = PDFGenerator(begin_date, end_date, category)
    begin_date: datetime.datetime, begin date of digest
    end_date: datetime.datetime, end date of digest
    category: list, categories of news to retrieve

    available functions:
    generate_pdf(): creates pdf file at parser_app/pdfs folder and returns it's filename in str format. If no news found
    returns None

    """

    class PDFGeneratorException(Exception):
        pass

    def __init__(self, begin_date, end_date, category):
        assert type(category) is list
        self.begin_date = begin_date
        self.end_date = end_date
        self.category = category

    def _db_query(self):
        category_id = Category.objects.filter(category_name__in=self.category)
        return News.objects.filter(time__gte=self.begin_date, time__lte=self.end_date,
                                   category__in=category_id).order_by('time')

    def generate_pdf(self):
        bunch_of_news = self._db_query()

        if bunch_of_news:
            filename = "parser_app/pdfs/digest" + str(uuid.uuid4()) + ".pdf"

            doc = SimpleDocTemplate(filename,
                                    rightMargin=72, leftMargin=72,
                                    topMargin=72, bottomMargin=18)

            stylesheet = getSampleStyleSheet()
            stylesheet.add(ParagraphStyle(name='header', fontName="DejaVuSans-Bold", fontSize=14))
            stylesheet.add(ParagraphStyle(name='main_content', fontName="DejaVuSans", fontsize=12, alignment=4))
            stylesheet.add(
                ParagraphStyle(name='footer', fontName="DejaVuSans", fontsize=9, alignment=4, textColor='grey'))

            digest = []

            for news in bunch_of_news:
                try:
                    digest.append(Paragraph(news.title, stylesheet['header']))
                    digest.append(Spacer(1, 6))
                    digest.append(Paragraph(escape(news.description), stylesheet['main_content']))
                    digest.append(Spacer(1, 3))
                    digest.append(Paragraph(news.time.strftime("%d %B %Y %H:%M") + ' ' + news.category.category_name,
                                            stylesheet['footer']))
                    digest.append(Spacer(1, 12))
                except Exception as e:
                    raise self.PDFGeneratorException('Can not generate PDF:', e.args) from e

            doc.build(digest)

            print("[PDFGenerator]:Pdf {0} generated".format(filename))
            return filename
        else:
            print("[PDFGenerator]: No news for requested period found")

            return None
