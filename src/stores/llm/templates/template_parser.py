import os
import string

class TemplateParser:
    def __init__(self, language: str = None, default_language="en"):
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.default_language = default_language
        self.language = None
        self.set_lang(language)

    def set_lang(self, language: str):
        # If no language provided, use default
        if not language:
            self.language = self.default_language
            return

        language_path = os.path.join(self.current_path, "locales", language)
        if os.path.exists(language_path):
            self.language = language
        else:
            self.language = self.default_language

    def get(self, group: str, key: str, vars: dict = {}):
        if not group or not key:
            return None

        # Ensure we always have a language
        if not self.language:
            self.language = self.default_language

        group_path = os.path.join(self.current_path, "locales", self.language, f"{group}.py")
        targeted_language = self.language

        if not os.path.exists(group_path):
            group_path = os.path.join(self.current_path, "locales", self.default_language, f"{group}.py")
            targeted_language = self.default_language

        if not os.path.exists(group_path):
            return None

        # Import the correct locale module
        module = __import__(f"stores.llm.templates.locales.{targeted_language}.{group}", fromlist=[group])
        if not module:
            return None

        key_attr = getattr(module, key, None)
        if not key_attr:
            return None

        # Support string.Template substitution
        return key_attr.substitute(vars) if isinstance(key_attr, string.Template) else key_attr
