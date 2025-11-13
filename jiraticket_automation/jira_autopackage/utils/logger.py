import logging

logger = logging.getLogger("jiraticket_automation")
logger.setLevel(logger.DEBUG)

file_handler = logging.FileHandler("logs/automation.log")

