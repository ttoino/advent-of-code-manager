#!/usr/bin/env python3
from pathlib import Path
from shutil import copy
from scraper import get_available_events, get_daily_progress, get_description, get_input, get_progress, submit_answer
from configargparse import ArgumentParser
import subprocess


def events(args):
    events = get_available_events(args)

    print("Available events:\n")
    print('\n'.join(events))


def progress(args):
    progress = get_progress(args)

    print("Current progress:\n")
    print(progress)


def test(args):
    if subprocess.call([f"python3 part{args.part}.py"],
                       cwd=f"day{args.day:02}",
                       shell=True) != 0:
        return

    outf = open(f"day{int(args.day):02}/part{args.part}.out")
    answer = outf.readline().strip()
    outf.close()

    print(answer)


def submit(args):
    if subprocess.call([f"python3 part{args.part}.py"],
                       cwd=f"day{args.day:02}",
                       shell=True) != 0:
        return

    outf = open(f"day{int(args.day):02}/part{args.part}.out")
    answer = outf.readline().strip()
    outf.close()

    print(submit_answer(args, answer))

    update(args)


def get(args):
    p = Path(f"day{int(args.day):02}/")
    p.mkdir(exist_ok=True)

    if not (p / "README.md").exists():
        desc = get_description(args)
        with open(str(p / "README.md"), "w") as f:
            f.write(desc)

    if not (p / "input").exists():
        inp = get_input(args)
        with open(str(p / "input"), "w") as f:
            f.write(inp)

    templates = Path(__file__).parent / "templates"
    if not (p / "part1.py").exists():
        copy(templates / "part1.py", p / "part1.py")
    if not (p / "part2.py").exists():
        copy(templates / "part2.py", p / "part2.py")


def update(args):
    f = open("README.md", "r")
    fd = f.read()
    f.close()

    fd = fd.replace("{year}", args.year)

    p = get_daily_progress(args)
    for i in range(1, 26):
        fd = fd.replace(f"{{day{i:02}}}", p[i])

    f = open("README.md", "w")
    f.write(fd)
    f.close()

    if args.day:
        get(args)
        desc = get_description(args)
        with open(f"day{int(args.day):02}/README.md", "w") as f:
            f.write(desc)


def init(args):
    if args.year is None:
        events = list(get_available_events(args))

        print("Available events:\n")
        print('\n'.join(events))

        event = input("\nSelect event: ")

        while event.strip() not in events:
            event = input("Select event: ")

        args.year = event

    if args.session is None:
        args.session = input("Enter your session cookie: ")

    with open(".aocm", "w") as cfg_file:
        cfg_file.write(f"year={args.year}\nsession={args.session}\n")

    templates = Path(__file__).parent / "templates"
    copy(templates / "README.md", "README.md")
    copy(templates / "LICENSE", "LICENSE")
    copy(templates / ".gitignore", ".gitignore")

    update(args)

    for i in range(1, 26):
        print(f"\r\x1B[KGetting day {i}!", end="")

        args.day = i
        get(args)

    print(f"\r\x1B[KDone!")


def create_parser():
    parser = ArgumentParser(prog="aocm", default_config_files=[".aocm"])
    parser.add_argument("--session", help="Session cookie")
    parser.add_argument("--year", help="Advent of code year")
    parser.set_defaults(func=lambda x: parser.print_help())

    subparsers = parser.add_subparsers()

    parser_init = subparsers.add_parser("init")
    parser_init.set_defaults(func=init)

    parser_update = subparsers.add_parser("update")
    parser_update.set_defaults(func=update)
    parser_update.add_argument("day", type=int, nargs="?")

    parser_events = subparsers.add_parser("events")
    parser_events.set_defaults(func=events)

    parser_progress = subparsers.add_parser("progress")
    parser_progress.set_defaults(func=progress)

    parser_submit = subparsers.add_parser("submit")
    parser_submit.set_defaults(func=submit)
    parser_submit.add_argument("day", type=int)
    parser_submit.add_argument("part", choices=["1", "2"])

    parser_test = subparsers.add_parser("test")
    parser_test.set_defaults(func=test)
    parser_test.add_argument("day", type=int)
    parser_test.add_argument("part", choices=["1", "2"])

    parser_get = subparsers.add_parser("get")
    parser_get.set_defaults(func=get)
    parser_get.add_argument("day", type=int)

    return parser


def main():
    args = create_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
