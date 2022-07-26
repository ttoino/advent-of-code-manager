from bs4 import BeautifulSoup
import requests
from html2md import html2md


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
        c.decompose()

    return calendar.text


def get_description(args):
    scraper = create_scraper(
        args, f"https://adventofcode.com/{args.year}/day/{args.day}")
    descs = scraper.select("article.day-desc")

    desc = html2md(descs[0], 1)

    if len(descs) > 1:
        desc += "\n" + html2md(descs[1], 2)

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
                      "level": args.day,
                      "answer": answer
                  })
    scraper = BeautifulSoup(res.content, "html.parser")
    p = scraper.select_one("article > p")
    for a in p.select("a"):
        a.decompose()

    return p.text
