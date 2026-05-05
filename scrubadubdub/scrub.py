import re
import json
import xml.etree.ElementTree as ET
from typing import Union
import spacy


class Scrub:
    def __init__(self, conf):
        self.debug = False
        # Load Spacy NLP model
        self.nlp = spacy.load(conf.get('model'))
        self.label = conf.get('entity_label')
        #self.nlp = de_core_news_lg.load()
        self.replace = conf.get('replace')
        pcustom = conf.get('pattern')
        for key, pattern in pcustom.items():
            self.patterns[key] = pattern

    def print_debug(self, message):
        if self.debug:
            print(message)

    
    def scrub_text(self, text: str) -> str:
        scrubbed_text = text
        for category, pattern in self.patterns.items():
            if category == "phone":
                matches = re.finditer(pattern, scrubbed_text)
                for match in matches:
                    matched_phone = match.group(0)
                    # Remove parentheses from matched phone numbers
                    matched_phone = re.sub(r"^\((\d{3})\)$", r"\1", matched_phone)
                    scrubbed_text = scrubbed_text.replace(matched_phone, self.replace+"-PHONE")
            else:
                scrubbed_text = re.sub(pattern, self.replace+"-EX", scrubbed_text)

        scrubbed_text = self.scrub_pii_with_nlp(scrubbed_text)
        return scrubbed_text

    def scrub_pii_with_nlp(self, text: str) -> str:
        nlp_doc = self.nlp(text)
        final_text = text
        for name in nlp_doc.ents:
            self.print_debug(f"Entity: {name.text}  Label: {name.label_}")
            if name.label_ in self.label:
                final_text = re.sub(re.escape(name.text), self.replace, final_text)
        return final_text

    def scrub(
        self, input_data: Union[str, dict], original_format: str = "txt"
    ) -> Union[str, dict]:
        if original_format == "json":
            scrubbed_data = json.loads(input_data)
            scrubbed_data = self.scrub_dict(scrubbed_data)
        elif original_format == "ndjson":
            scrubbed_data = [
                self.scrub_dict(json.loads(line)) for line in input_data.splitlines()
            ]
        elif original_format == "xml":
            root = ET.fromstring(input_data)
            self.scrub_xml(root)
            scrubbed_data = ET.tostring(root, encoding="unicode")
        else:
            scrubbed_data = self.scrub_text(input_data)
        return scrubbed_data

    def scrub_dict(self, data: dict) -> dict:
        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = self.scrub_dict(value)
            elif isinstance(value, list):
                data[key] = [
                    self.scrub_dict(item) if isinstance(item, dict) else item
                    for item in value
                ]
            elif isinstance(value, str):
                data[key] = self.scrub_text(value)
        return data

    def scrub_xml(self, node: ET.Element) -> None:
        if node.text is not None:
            node.text = self.scrub_text(node.text)
        for child in node:
            self.scrub_xml(child)

