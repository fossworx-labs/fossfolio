import glob
from config import BASE_DIR, DOMAIN_NAME
import xml.etree.ElementTree as ET
from typing import Optional, List, Dict


def prettify_xml(xml_content: str) -> str:
    element = ET.fromstring(xml_content)
    ET.indent(element, space="  ")
    return ET.tostring(element, encoding="unicode", method="xml")


def create_sitemap(*args: Optional[List], **kwargs: Optional[Dict]) -> str:
    files_list: List[str] = list(
        glob.glob(str(BASE_DIR / "build/**/*.*"), recursive=True)
    )

    files_list = list(
        filter(lambda x: f"{DOMAIN_NAME}/sitemap.xml" not in x, files_list)
    )

    header: str = '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    footer: str = "</sitemapindex>"
    PARENT_DIR: str = "build/"
    content: str = "".join(
        f"<sitemap><loc>{DOMAIN_NAME}/{i[i.index(PARENT_DIR)+len(PARENT_DIR):]}</loc></sitemap>"
        for i in files_list
    )

    content = header + content + footer

    return prettify_xml(content)


def write_sitemap(
    sitemap_content: str, *args: Optional[List], **kwargs: Optional[Dict]
) -> None:
    with open(str(BASE_DIR / "build/sitemap.xml"), "w") as sitemap_file:
        sitemap_file.write(sitemap_content)


def generate_sitemap():
    write_sitemap(create_sitemap())


if __name__ == "__main__":
    generate_sitemap()
