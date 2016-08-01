import parser_app.utils as utils


from celery import shared_task
from celery.utils.log import get_task_logger


from .rss_overlord import RSSOverlord
from .pdf_overlord import PDFGenerator
from .email_overlord import EmailOverlord


logger = get_task_logger(__name__)

@shared_task(name="update_feed_task")
def update_feed_task():
    """Periodic task; updates rss feeds every 15 minutes"""
    overl = RSSOverlord()
    logger.info("RSS-feed has been updated")
    return overl.update_feed()

@shared_task(name="generate_pdf")
def generate_pdf(begin_date, end_date, category):
    pdfgen = PDFGenerator(begin_date=begin_date, end_date=end_date, category=category)
    return pdfgen.generate_pdf()

@shared_task(name="send_email")
def send_email_task(filename, send_to):
    emailoverl = EmailOverlord()
    emailoverl.send_mail(send_to=send_to, file=filename)
    return filename

@shared_task(name="clean pdfs folder")
def clean_pdfs_task(filename):
    return utils.clean_pdfs(filename)

@shared_task(name="generate_and_send")
def generate_and_send(begin_date, end_date, category, email):
    taskchain = generate_pdf.s(begin_date, end_date, category) | send_email_task.s(email) | clean_pdfs_task.s()
    taskchain()
