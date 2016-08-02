from news_parser.celery import app
from celery.utils.log import get_task_logger


from parser_app.rss_overlord import RSSOverlord

logger = get_task_logger(__name__)

@app.task(name="update_feed_task")
def update_feed_task():
    """updates rss feeds every 15 minutes"""
    overl = RSSOverlord()
    logger.info("RSS-feed has been updated")
    return overl.update_feed()