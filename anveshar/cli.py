"""Anveshar command line interface.

    concord run --cancer "renal medullary carcinoma" --discovery --out report.html
    concord run --cancer "rectal neuroendocrine tumor" --profile examples/profiles/pereira_msi_braf.json --out report.html
"""
import argparse
import sys


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="anveshar",
        description="A translational board for rare cancers and rare diseases: match a "
                    "condition and a patient's molecular profile to therapies validated "
                    "elsewhere, and generate novel cross-condition hypotheses.")
    sub = p.add_subparsers(dest="cmd")

    r = sub.add_parser("run", help="assemble and render a Anveshar report")
    r.add_argument("--cancer", required=True, help="condition name, e.g. 'renal medullary carcinoma'")
    r.add_argument("--profile", default=None, help="patient molecular profile json")
    r.add_argument("--scrna", default=None, help="path to an .h5ad for expressed target readout")
    r.add_argument("--no-discovery", action="store_true", help="skip the novel hypothesis layer")
    r.add_argument("--live", action="store_true", help="assemble via the Claude API when no curated file exists (needs ANTHROPIC_API_KEY)")
    r.add_argument("--model", default=None, help="model id for live assembly")
    r.add_argument("--out", default="concord_report.html", help="output HTML path")

    a = sub.add_parser("analyze", help="run the reproducible pipeline harness on a rare cancer")
    a.add_argument("--cancer", required=True, help="rare cancer name, e.g. 'renal medullary carcinoma'")
    a.add_argument("--live", action="store_true", help="query live databases (Open Targets, PubMed) as well as local knowledge")
    a.add_argument("--out", default=None, help="write the full dossier json to this path")

    sub.add_parser("version", help="print the Anveshar version")
    sub.add_parser("list", help="list the conditions Anveshar has curated knowledge for")

    args = p.parse_args(argv)

    if args.cmd == "analyze":
        import json
        from .pipeline import run as prun
        d = prun(args.cancer, live=args.live)
        if not d["resolved"]:
            print(f"concord: no rare cancer matched '{args.cancer}'", file=sys.stderr)
            return 2
        s = d["summary"]; bc = s["best_confidence"]
        print(f"Anveshar dossier for {d['condition']} ({d['mode']} mode): "
              f"drivers {', '.join(d['drivers']) or 'none'}; "
              f"{s['n_actionable']} borrowable approved therapies "
              f"({s['n_tissue_agnostic']} tissue agnostic), "
              f"{s['n_cross_condition']} shared driver candidates; "
              f"best confidence {bc['label'] + ' ' + str(bc['pct']) + '%' if bc else 'n/a'}.")
        print(d["disclaimer"])
        if args.out:
            json.dump(d, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            print(f"wrote {args.out}")
        return 0

    if args.cmd == "version":
        from . import __version__
        print(__version__)
        return 0

    if args.cmd == "list":
        import os
        from .engine import SLUGS, EXAMPLES
        for name, fname in sorted(SLUGS.items()):
            if os.path.exists(os.path.join(EXAMPLES, fname)):
                print(name)
        return 0

    if args.cmd == "run":
        from .engine import run
        try:
            data = run(args.cancer, profile=args.profile, scrna=args.scrna,
                       discovery=not args.no_discovery, out=args.out,
                       live=args.live, model=args.model)
        except ValueError as e:
            print(f"concord: {e}", file=sys.stderr)
            return 2
        print(f"Anveshar report for {data['cancer']['name']}: "
              f"{len(data.get('therapies', []))} therapies, "
              f"{len(data.get('discovery', []))} novel hypotheses, "
              f"written to {args.out}")
        return 0

    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
