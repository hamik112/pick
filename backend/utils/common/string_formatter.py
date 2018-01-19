__author__ = 'parkjiminy'

import ast

import traceback

import logging
logger = logging.getLogger(__name__)

def string_to_literal(data):
	try:
		return ast.literal_eval(data)
	except Exception:
		return []
