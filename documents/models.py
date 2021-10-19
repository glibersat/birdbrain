from urllib.parse import urljoin

import markdown
from bs4 import BeautifulSoup, Comment
from django.db import models
from django.utils import timezone
from markdown_link_attr_modifier import LinkAttrModifierExtension
from markdownify import markdownify


class Document(models.Model):
    created_on = models.DateTimeField(default=timezone.now)
    uri = models.URLField(unique=True)
    content_raw = models.TextField(blank=True)
    content_plain = models.TextField(blank=True)

    @property
    def title(self):
        soup = BeautifulSoup(self.content_raw, "lxml")
        return soup.title.get_text()

    @property
    def content_markdown(self):
        soup = BeautifulSoup(self.content_raw, "lxml")
        soup = soup.find("body")
        for s in soup(
            ["aside", "header", "iframe", "script", "footer", "nav", "style", "form"]
        ):
            s.extract()

        # Remove invisible things
        for s in soup.findAll("", {"aria-hidden": "true"}):
            s.extract()

        styles = (
            '[style="display:none;"]',
            '[style="display: none;"]',
            '[style="visibility:hidden;"]',
            '[style="visibility: hidden;"]',
        )
        for style in styles:
            for s in soup.select(style):
                s.extract()

        # Make absolute URLS
        for element in soup.find_all(href=True):
            element["href"] = urljoin(self.uri, element.get("href"))

        # Strip comments
        for element in soup.findAll(text=lambda text: isinstance(text, Comment)):
            element.extract()

        return markdown.markdown(
            markdownify(str(soup)),
            extensions=[
                LinkAttrModifierExtension(new_tab="on", no_referrer="external_only")
            ],
        )

    def __str__(self):
        return self.title
