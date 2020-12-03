import datetime
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from dataclasses import dataclass

PATH_TO_TEMPLATES = Path('TEMPLATES/')
PATH_TO_RESOURCES = Path('../generator/RESOURCES/')
PATH_TO_OUTPUT = Path('../docs/')
URL_ROOT = "https://sybarite.cz/"

link_to_homepage = "/"  # TODO: always / in production
html_file_suffix = ".html"


@dataclass()
class Page(object):
    title: str
    keywords: str
    description: str
    content_file: str
    url: str
    language: str
    last_mod: datetime.datetime

    def keys(self):
        """Get keys that allows conversion of this class to dictionary.

        Returns:
            List[str]: List of the keys to be passed to template.
        """
        return ['title', 'keywords', 'description', 'url', 'content_file',
                'language']

    def __getitem__(self, key):
        """Allows conversion of this class to dictionary.
        """
        return getattr(self, key)

    def generate_site(self):
        with open(PATH_TO_TEMPLATES.joinpath('page.html')) as tem_han:
            template = Environment(
                loader=FileSystemLoader(PATH_TO_TEMPLATES)
            ).from_string(tem_han.read())
            html_str = template.render(
                **dict(self),
                link_to_homepage=link_to_homepage
            )
            return html_str

    @property
    def absolute_url(self):
        if self.url != 'index':
            return URL_ROOT + self.url + html_file_suffix
        return URL_ROOT

    @property
    def last_modified(self):
        if self.last_mod is None:
            return None
        return self.last_mod.strftime('%Y-%m-%d')


pages = [
    Page(title="Webové stránky Sybarite | řešení, která vydělají",
         keywords="webové stránky, online projekty, SEO optimalizace, responzivní design, mobilní zařízení, Seznam.cz, Google.com",  # noqa: E501
         description="Společnost Sybarite s.r.o. má rozsáhlou zkušenost s tvorbou webových stránek pro firmy i jednotlivce. Nabízíme on-line řešení, která vám vydělají peníze.",  # noqa: E501
         url="index",
         content_file='page_domu.html',
         language="cs",
         last_mod=datetime.datetime(2020, 11, 7)
         ),
    Page(title="Webové stránky Sybarite | poskytované služby",
         keywords="webové stránky, online projekty, SEO optimalizace, responzivní design, mobilní zařízení, Seznam.cz, Google.com",  # noqa: E501
         description="Společnost Sybarite s.r.o. má rozsáhlou zkušenost s tvorbou webových stránek pro firmy i jednotlivce. Nabízíme on-line řešení, která vám vydělají peníze.",  # noqa: E501
         url="sluzby",
         content_file='page_sluzby.html',
         language="cs",
         last_mod=datetime.datetime(2020, 11, 7)
         ),
    Page(title="Webové stránky Sybarite | projekty",
         keywords="webové stránky, online projekty, SEO optimalizace, responzivní design, mobilní zařízení, Seznam.cz, Google.com",  # noqa: E501
         description="Společnost Sybarite s.r.o. má rozsáhlou zkušenost s tvorbou webových stránek pro firmy i jednotlivce. Nabízíme on-line řešení, která vám vydělají peníze.",  # noqa: E501
         url="projekty",
         content_file='page_projekty.html',
         language="cs",
         last_mod=datetime.datetime(2020, 11, 7)
         ),
    Page(title="Webové stránky Sybarite | kontaktní informace",
         keywords="webové stránky, online projekty, SEO optimalizace, responzivní design, mobilní zařízení, Seznam.cz, Google.com",  # noqa: E501
         description="Společnost Sybarite s.r.o. má rozsáhlou zkušenost s tvorbou webových stránek pro firmy i jednotlivce. Nabízíme on-line řešení, která vám vydělají peníze.",  # noqa: E501
         url="kontakt",
         content_file='page_kontakt.html',
         language="cs",
         last_mod=datetime.datetime(2020, 11, 7)
         ),
    Page(title="Webové stránky Sybarite | Sybarite company",
         keywords="webové stránky, online projekty, SEO optimalizace, responzivní design, mobilní zařízení, Seznam.cz, Google.com",  # noqa: E501
         description="Společnost Sybarite s.r.o. má rozsáhlou zkušenost s tvorbou webových stránek pro firmy i jednotlivce. Nabízíme on-line řešení, která vám vydělají peníze.",  # noqa: E501
         url="english",
         content_file='page_english.html',
         language="en",
         last_mod=datetime.datetime(2020, 11, 7)
         ),
    Page(title="Webové stránky Sybarite | reference",
         keywords="webové stránky, online projekty, SEO optimalizace, responzivní design, mobilní zařízení, Seznam.cz, Google.com",  # noqa: E501
         description="Společnost Sybarite s.r.o. má rozsáhlou zkušenost s tvorbou webových stránek pro firmy i jednotlivce. Nabízíme on-line řešení, která vám vydělají peníze.",  # noqa: E501
         url="reference",
         content_file='page_reference.html',
         language="cs",
         last_mod=datetime.datetime(2020, 11, 7)
         )
]

# Remove all existing resources
if PATH_TO_OUTPUT.exists():
    shutil.rmtree(PATH_TO_OUTPUT)

# Create new dir
PATH_TO_OUTPUT.mkdir()

for page in pages:
    content = page.generate_site()
    with PATH_TO_OUTPUT.joinpath(page.url + html_file_suffix).open('w') as fp:
        fp.write(content)

# Copy resources
shutil.copytree(PATH_TO_RESOURCES, PATH_TO_OUTPUT, dirs_exist_ok=True)

# Generate resource map:
with open(PATH_TO_TEMPLATES.joinpath('site_map.xml')) as tem_han:
    template = Environment(
        loader=FileSystemLoader(PATH_TO_TEMPLATES)
    ).from_string(tem_han.read())
    html_str = template.render(
        sites=pages
    )
    with PATH_TO_OUTPUT.joinpath('sitemap.xml').open('w') as f_xml:
        f_xml.write(html_str)

robots_txt_content = f"""User-agent: *
Allow: /
Sitemap: {URL_ROOT}/sitemap.xml"""
with PATH_TO_OUTPUT.joinpath('robots.txt').open('w') as robots_txt_h:
    robots_txt_h.write(robots_txt_content)
