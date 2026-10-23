import argparse
import json
import queue
import signal
import subprocess
import sys
import threading


def get_json(args):
    return json.loads(
        subprocess.run(args, capture_output=True, text=True).stdout
    )


def decide():
    if get_json(["niri", "msg", "--json", "overview-state"])["is_open"]:
        return "uncovered"
    if get_json(["niri", "msg", "--json", "focused-window"]) is None:
        return "uncovered"
    return "covered"


def pump(events):
    proc = subprocess.Popen(
        ["niri", "msg", "--json", "event-stream"], stdout=subprocess.PIPE
    )

    assert proc.stdout is not None

    for x in proc.stdout:
        events.put(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--covered", required=True)
    ap.add_argument("-u", "--uncovered", required=True)
    ap.add_argument("-i", "--init")
    ap.add_argument("-q", "--quit")
    args = ap.parse_args()

    def on_quit(signum, frame):
        if args.quit:
            subprocess.run(args.quit, shell=True)
        sys.exit(0)

    signal.signal(signal.SIGINT, on_quit)
    signal.signal(signal.SIGTERM, on_quit)

    cmds = {"covered": args.covered, "uncovered": args.uncovered}

    def run(state):
        subprocess.run(cmds[state], shell=True)

    current = None

    if args.init:
        subprocess.run(args.init, shell=True)
    else:
        current = decide()
        run(current)

    events = queue.Queue()
    threading.Thread(target=pump, args=(events,), daemon=True).start()

    while True:
        events.get()
        want = decide()
        if want != current:
            run(want)
            current = want


if __name__ == "__main__":
    main()
