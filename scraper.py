from bs4 import BeautifulSoup
import requests
from html2md import html2md
import re


def request(args, method: str, url: str, **kwargs):
    return requests.request(method,
                            url,
                            cookies={"session": args.session},
                            **kwargs)


def create_scraper(args, url: str):
    res = request(args, "get", url)
    scraper = BeautifulSoup(res.content, "html.parser")

    return scraper


def get_available_events(args):
    scraper = create_scraper(args, "https://adventofcode.com/events")

    return (y.text.removeprefix("[").removesuffix("]")
            for y in scraper.select(".eventlist-event > a"))


def get_progress(args):
    scraper = create_scraper(args, f"https://adventofcode.com/{args.year}")
    calendar = scraper.select_one(".calendar")

    for c in calendar.select(
            ":not(:is(.calendar-verycomplete, .calendar-complete)) > .calendar-mark-complete,"
            ":not(.calendar-verycomplete) > .calendar-mark-verycomplete"):
        c.replace_with(" ")

    return calendar.text


def get_daily_progress(args):
    p = get_progress(args).splitlines()

    return {
        int(d[0]): i[-2:].replace(" ", "☆").replace("*", "★")
        for i in p
        if (d := re.search(r"\d{1,2}", i))
    }


def get_description(args):
    base_url = f"https://adventofcode.com/{args.year}/day/{args.day}"
    scraper = create_scraper(args, base_url)
    descs = scraper.select("article.day-desc")

    desc = html2md(descs[0], 1, base_url)

    if len(descs) > 1:
        desc += "\n" + html2md(descs[1], 2, base_url)

    return desc


def get_input(args):
    res = request(args, "get",
                  f"https://adventofcode.com/{args.year}/day/{args.day}/input")
    return res.text


def submit_answer(args, answer):
    res = request(args,
                  "post",
                  f"https://adventofcode.com/{args.year}/day/{args.day}/answer",
                  data={
                      "level": args.part,
                      "answer": answer
                  })
    scraper = BeautifulSoup(res.content, "html.parser")
    p = scraper.select_one("article > p")
    for a in p.select("a"):
        a.decompose()

    return p.text
