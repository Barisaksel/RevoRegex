
import re
import json
import os
from typing import Optional


class RegexMatcher:

    # Error messages loaded from error-messages.json
    _error_messages: dict = None

    @classmethod
    def _load_error_messages(cls) -> None:
        """
        Loads error messages from the error-messages.json file if not already loaded.
        """
        if cls._error_messages is not None:
            return
        json_path = os.path.join(os.path.dirname(__file__), 'error-messages.json')
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                cls._error_messages = json.load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load error-messages.json: {e}")

    def _msg(self, key: str, **kwargs) -> str:
        self._load_error_messages()
        lang = self.language if self.language in self._error_messages else 'en'
        msg = self._error_messages[lang].get(key, self._error_messages['en'].get(key, key))
        return msg.format(**kwargs)
    """
    Multilingual regex validation and matching utility.

    Features:
        - Supports multiple languages (patterns loaded from language-regex.json)
        - Advanced validation (IBAN, credit card, IP, etc.)
        - Extensible: add new languages/patterns at runtime
        - Utility methods for listing languages and pattern keys
    """
    _patterns: dict = None

    @classmethod
    def _load_patterns(cls) -> None:
        """
        Loads regex patterns from the language-regex.json file if not already loaded.
        Raises RuntimeError if loading fails.
        """
        if cls._patterns is not None:
            return
        json_path = os.path.join(os.path.dirname(__file__), 'language-regex.json')
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                cls._patterns = json.load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load language-regex.json: {e}")

    @classmethod
    def reload_patterns(cls) -> None:
        """
        Force reload of regex patterns from the language-regex.json file.
        """
        cls._patterns = None
        cls._load_patterns()

    @classmethod
    def list_languages(cls) -> list:
        """
        Returns a list of supported language codes.
        """
        cls._load_patterns()
        return list(cls._patterns.keys())

    @classmethod
    def list_patterns(cls, language: str = None) -> list:
        """
        Returns a list of available pattern keys for a given language.
        If language is None, uses the default ('en').
        """
        cls._load_patterns()
        lang = language or 'en'
        if lang not in cls._patterns:
            raise ValueError(f"Language '{lang}' not supported.")
        return list(cls._patterns[lang].keys())

    def __init__(self, language: str = 'en'):
        """
        Initialize a RegexMatcher for a specific language.
        :param language: Language code (e.g., 'en', 'tr')
        :raises ValueError: If language is not supported
        """
        self._load_patterns()
        if language not in self._patterns:
            raise ValueError(f"Language '{language}' not supported.")
        self.language = language


    def match(self, pattern_key: str, text: str) -> Optional[re.Match]:
        """
        Returns a regex match object if the text matches the pattern for the given key, else None.
        :param pattern_key: Pattern key (e.g., 'email', 'phone')
        :param text: Text to match
        :raises ValueError: If pattern key is not found
        """
        pattern = self._patterns.get(self.language, {}).get(pattern_key)
        if not pattern:
            raise ValueError(f"Pattern key '{pattern_key}' not found for language '{self.language}'.")
        return re.match(pattern, text)


    def validate_with_message(self, pattern_key: str, text: str) -> tuple[bool, Optional[str]]:
        """
        Validates the text against the pattern for the given key.
        Returns (True, None) if valid, (False, error_message) if not valid.
        Error messages are returned in the selected language if available.
        """
        pattern = self._patterns.get(self.language, {}).get(pattern_key)
        if not pattern:
            return False, self._msg('pattern_not_found', pattern_key=pattern_key, language=self.language)
        if not re.fullmatch(pattern, text):
            return False, self._msg('invalid_format')
        # IP address validation
        if pattern_key in ["ip", "ip_address"]:
            try:
                parts = text.split('.')
                if len(parts) != 4:
                    return False, self._msg('ip_octet_count')
                for part in parts:
                    if not part.isdigit() or not 0 <= int(part) <= 255:
                        return False, self._msg('ip_octet_range', part=part)
            except Exception:
                return False, self._msg('ip_error')
        # IBAN validity (mod-97)
        if pattern_key in ["iban"]:
            iban = text.replace(' ', '').upper()
            iban_rearranged = iban[4:] + iban[:4]
            iban_numeric = ''
            for c in iban_rearranged:
                if c.isdigit():
                    iban_numeric += c
                elif c.isalpha():
                    iban_numeric += str(ord(c) - 55)
                else:
                    return False, self._msg('iban_invalid_char')
            try:
                if int(iban_numeric) % 97 != 1:
                    return False, self._msg('iban_mod97')
            except Exception:
                return False, self._msg('iban_error')
        # Credit card Luhn algorithm
        if pattern_key in ["credit_card", "kredi_kartı"]:
            digits = [int(d) for d in text if d.isdigit()]
            if not digits:
                return False, self._msg('cc_digits')
            total = 0
            reverse_digits = digits[::-1]
            for i, d in enumerate(reverse_digits):
                if i % 2 == 1:
                    doubled = d * 2
                    total += doubled - 9 if doubled > 9 else doubled
                else:
                    total += d
            if total % 10 != 0:
                return False, self._msg('cc_luhn')
        return True, None


    def validate(self, pattern_key: str, text: str) -> bool:
        """
        Returns True if valid, False if not. (For backward compatibility)
        :param pattern_key: Pattern key
        :param text: Text to validate
        :return: bool
        """
        valid, _ = self.validate_with_message(pattern_key, text)
        return valid


    @classmethod
    def add_language(cls, lang: str, patterns: dict) -> None:
        """
        Add a new language and its pattern dictionary at runtime.
        :param lang: Language code
        :param patterns: Dictionary of pattern_key: regex
        """
        cls._load_patterns()
        cls._patterns[lang] = patterns
