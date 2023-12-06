import sys
import json
from lxml import etree
from haruka_parser.extract import extract_text
from haruka_parser.extract import DEFAULT_CONFIG as configuration


def get_one(ele, all=False):
    if not ele or not isinstance(ele, list):
        return None
    if isinstance(ele[0], etree._Element):
        if all:
            return [
                etree.tostring(i, method="html", encoding="utf-8").decode() for i in ele
            ]
        return etree.tostring(ele[0], method="html", encoding="utf-8").decode()
    else:
        if all:
            return [i.strip() for i in ele]
        return ele[0].strip()


def parse_cnki(detail):
    if "<!--brief end-->" in detail:
        detail = detail.replace("<!--reference start-->", "</div>")
        if detail.count("--brief start--") == 2:
            detail = detail.replace("<!--brief start-->", "", 1).replace(
                "<!--brief start-->", '<div id="start">'
            )
        else:
            return "不完整"
    tree = etree.HTML(detail)
    etree.strip_elements(tree, *["style", "script"])
    abstract_zh = get_one(
        tree.xpath("//div[@id='a_abstract']/p[@id='b-abstract']/span/text()")
    )
    abstract = get_one(
        tree.xpath("//div[@class='content']/div[@id='a_abstractEN']/p/text()")
    )
    content = get_one(tree.xpath('//div[@id="start"]'), all=True)
    doi = (
        "".join(tree.xpath("//div[@class='content']/div[@class='tips']/text()"))
        .replace(" ", "")
        .strip()
    )
    imgs = tree.xpath(
        "//div[@class='content']//img[@alt='正在加载图片']/@data-src|//div[@class='content']//img[contains(@src,'Detail/GetImg')]/@src"
    )
    literature_ele_list = tree.xpath(
        "//div[@id='a_bibliography']/p/a[contains(@id,'bibliography_')]"
    )
    reference = []
    for literature in literature_ele_list:
        wx = "".join(literature.xpath("./text()")).strip().replace("  ", "").strip()
        if wx:
            tmp_dict = {}
            tmp_dict["raw"] = wx
            reference.append(tmp_dict)
    dir_tree = (
        "".join(tree.xpath("//dl[@class='sidenav-list']/dd[@class='guide']//text()"))
        .strip()
        .strip("参考文献")
    )
    organization_list = tree.xpath(
        "//div[@class='content']/h2/a[@id='InfoOrgId']/text()"
    )
    keywords_zh = (
        "".join(
            tree.xpath(
                "//div[@id='a_keywords']/p[@id='b_keywords']/span/a[@class='keyprogram']/text()"
            )
        )
        .replace("；", ";")
        .replace(" ", "")
    )
    keywords = (
        "".join(tree.xpath("//div[@id='a_keywordsEN']/p/a/text()"))
        .replace("；", ";")
        .replace(" ", "")
    )
    intro = "".join(tree.xpath("//div[@class='brief']/p[@id='briefId']/span/text()"))
    j_date = get_one(
        tree.xpath(
            "//div[@class='content']/div[@class='brief']/p/b[text()='收稿日期：']/parent::p/text()"
        )
    )

    authors = tree.xpath("//h2[@id='authorsId']/a[@id='authorId']/text()")
    attachs = []
    attachs_tree = tree.xpath("//div[@class='zq-inner']/h6[@class='zq-title']/a")
    if attachs_tree:
        for attach in attachs_tree:
            tmp_dict = {}
            tmp_dict["title"] = get_one(attach.xpath("./text()"))
            tmp_dict["href"] = get_one(attach.xpath("./@href"))
            attachs.append(tmp_dict)
    foot_note = [
        "".join(foot.xpath(".//text()")).replace("  ", "").strip()
        for foot in tree.xpath("//div[@id='a_footnote']/p/span")
    ]
    title_zh = get_one(tree.xpath("//h1[@id='topTitle']/span/text()"))
    title = get_one(tree.xpath("//h1[@id='EngTitle']/b/text()"))
    data = {
        "abstract_zh": abstract_zh,
        "abstract": abstract,
        "imgs": imgs,
        "reference": reference,
        "dir_tree": dir_tree,
        "organization_list": organization_list,
        "keywords_zh": keywords_zh,
        "keywords": keywords,
        "j_date": j_date,
        "intro": intro,
        "authors": authors,
        "title_zh": title_zh,
        "title": title,
        "attachs": attachs,
        "foot_note": foot_note,
        "doi": doi,
        "content": content,
    }
    return data


if __name__ == "__main__":
    html = open(sys.argv[1]).read()
    if "cnki" in sys.argv[1]:
        configuration["extract_cnki_latex"] = True
        data = parse_cnki(html)
        data["raw_content"] = "\n".join(
            [extract_text(i, configuration)[0] for i in data["content"]]
        ).replace("导出到EXCEL", "")
        data["content"] = (
            data["raw_content"]
            .replace("\\$", "[extract_itex]")
            .replace("$", "")
            .replace("[extract_itex]", "$")
        )
        # print(json.dumps(data, ensure_ascii=False))
        print(data["content"])
    else:
        a, info = extract_text(html, configuration)
        print(a, info)
