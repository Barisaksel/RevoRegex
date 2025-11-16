# __init__.py for revoregex package

from .matcher import RegexMatcher

class RevoRegex(RegexMatcher):
	def __init__(self, lang: str = 'en'):
		super().__init__(language=lang)
