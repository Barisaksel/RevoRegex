
# RevoRegex

**RevoRegex** is a professional, multilingual regex validation library for Python. It supports Turkish, English, German, and French out of the box, and is easily extendable to more languages and validation types. Patterns and error messages are fully modular and loaded from JSON, making it ideal for international projects and scalable applications.

## Features
- Multilingual regex validation (TR, EN, DE, FR)
- Language-specific error messages
- Advanced validation: IBAN (mod-97), credit card (Luhn), IP (range check)
- Easily extensible: add new languages or patterns via JSON
- Modular, maintainable, and production-ready
- Comprehensive test suite

## Installation
```bash
pip install revoregex
```

## Usage
```python
from revoregex import RegexMatcher

# Turkish example
matcher = RegexMatcher(language='tr')
valid, msg = matcher.validate_with_message('email', 'test@example.com')
print(valid, msg)  # True, None

# English example
matcher = RegexMatcher(language='en')
valid, msg = matcher.validate_with_message('phone', '+11234567890')
print(valid, msg)  # True, None

# German example
matcher = RegexMatcher(language='de')
valid, msg = matcher.validate_with_message('iban', 'DE89370400440532013000')
print(valid, msg)

# French example
matcher = RegexMatcher(language='fr')
valid, msg = matcher.validate_with_message('téléphone', '+33612345678')
print(valid, msg)
```

## Supported Validations
- Email, phone, IBAN, credit card, IP, domain, hex color, date, username, password, plate, postal code, JSON, HTML tag, UUID, MAC address, and more.

## Supported Languages
- Turkish (`tr`)
- English (`en`)
- German (`de`)
- French (`fr`)

## Extending
Add new languages or patterns by editing the `language-regex.json` and `error-messages.json` files. No code changes required.

## License
MIT

---

**PyPI Keywords:**
regex, validation, multilingual, internationalization, i18n, Turkish, English, German, French, IBAN, credit card, phone, email, domain, python, luhn, mod97, json, html, uuid, mac address, plate, password, username, open source, PyPI, form validation, data validation