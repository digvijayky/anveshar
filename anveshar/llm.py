"""Anveshar live assembly via the Claude API (Built with Claude).

Given a condition and evidence gathered from the connectors, ask Claude to synthesize a
cited DiseaseReport DATA dict, enforcing cite or abstain and the Anveshar schema. This is
the path that lets Anveshar assemble a report for a condition it has no curated file for.

Requires ANTHROPIC_API_KEY and the optional 'live' extra (anthropic). The pure helpers
(_build_prompt, _extract_json) are import free so they can be unit tested offline, and
synthesize_report accepts an injected client so it can be tested without the network.
"""
import os
import json
import re

from .schema import assert_no_dashes

DEFAULT_MODEL = "claude-sonnet-5"

SYSTEM = (
    "You are Anveshar's evidence synthesizer for rare cancers and rare diseases. "
    "You receive a condition and a bundle of real evidence (PubMed records and trials) and "
    "you output ONE JSON object, the Anveshar report DATA dict, and nothing else. "
    "Rules you must obey without exception: every therapy citation must be a real PMID, DOI, "
    "or NCT that appears in the provided evidence or that you are independently certain of; if "
    "you are not certain, omit the item or mark it UNVERIFIED rather than inventing a citation; "
    "grade each therapy by evidence tier (1 tissue agnostic approval, 2 approved elsewhere on a "
    "shared target or a basket signal, 3 mechanistic only); keep approved options separate from "
    "the discovery hypotheses; NEVER use an em dash or an en dash anywhere, use commas or "
    "parentheses or the word to; write American English."
)

SCHEMA_HINT = (
    "The DATA object must have these keys: cancer{name,sub,chips[3]}, "
    "voiceNote{patient,clinician,researcher}, overview{patient,clinician,researcher} (HTML <p> strings), "
    "targetsIntro{3 voices}, targets[{name,present_in,evidence}], therapiesIntro{3 voices}, "
    "therapies[{drug,target,tier(integer 1|2|3),modality,approved_in,dev_stage,"
    "rationale{patient,clinician,researcher},citation{label,url}}], trials[{nct,title,phase,intervention,eligibility,url}], "
    "precedentIntro{3 voices}, precedents[{biomarker,drug,year,citation{label,url}}], "
    "discoveryIntro{3 voices}, discovery[{hypothesis,shared,source,modality,rationale,transferability,prediction,citation{label,url}}], "
    "disclaimer. Every url is a real https link. Modalities must be one of: small molecule, antibody, "
    "antibody drug conjugate, bispecific T cell engager, cell therapy, gene therapy, antisense oligonucleotide, "
    "radioligand therapy, cytotoxic chemotherapy, immune checkpoint inhibitor, other."
)


def _build_prompt(condition: str, evidence: dict) -> str:
    """Compose the user prompt from the condition and gathered evidence (pure, testable)."""
    pubmed = evidence.get("pubmed", []) or []
    trials = evidence.get("trials", []) or []
    lines = [f"Condition: {condition}", "", "PubMed evidence (real records to cite):"]
    for r in pubmed[:25]:
        lines.append(f"- PMID {r.get('pmid','')}: {r.get('title','')} ({r.get('journal','')} {r.get('year','')})"
                     + (f" doi:{r.get('doi')}" if r.get("doi") else ""))
    lines.append("")
    lines.append("ClinicalTrials.gov (real trials to cite):")
    for t in trials[:20]:
        nct = t.get("nct", "") if isinstance(t, dict) else getattr(t, "nct", "")
        title = t.get("title", "") if isinstance(t, dict) else getattr(t, "title", "")
        lines.append(f"- {nct}: {title}")
    lines.append("")
    lines.append(SCHEMA_HINT)
    lines.append("")
    lines.append("Output only the JSON DATA object for this condition. Focus on therapies that "
                 "translate from other conditions sharing the same molecular dependency, and add a "
                 "discovery section of novel testable hypotheses. Cite or abstain.")
    return "\n".join(lines)


def _extract_json(text: str) -> dict:
    """Pull the first complete JSON object out of a model response (pure, testable)."""
    start = text.find("{")
    if start < 0:
        raise ValueError("no JSON object in model output")
    depth = 0
    in_str = False
    esc = False
    for i in range(start, len(text)):
        c = text[i]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return json.loads(text[start:i + 1])
    raise ValueError("unbalanced JSON in model output")


def _client():
    import anthropic  # lazy, only needed for a real call
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set; live assembly needs it")
    return anthropic.Anthropic(api_key=key)


def synthesize_report(condition: str, evidence: dict, model: str = DEFAULT_MODEL, client=None) -> dict:
    """Ask Claude to synthesize a validated Anveshar DATA dict from real evidence."""
    client = client or _client()
    msg = client.messages.create(
        model=model, max_tokens=8000, system=SYSTEM,
        messages=[{"role": "user", "content": _build_prompt(condition, evidence)}])
    text = "".join(getattr(b, "text", "") for b in msg.content if getattr(b, "type", "") == "text")
    data = _extract_json(text)
    # enforce the house style even on model output
    def scrub(o):
        if isinstance(o, str):
            return o.replace("—", ", ").replace("–", "-")
        if isinstance(o, list):
            return [scrub(x) for x in o]
        if isinstance(o, dict):
            return {k: scrub(v) for k, v in o.items()}
        return o
    data = scrub(data)
    assert_no_dashes(data)
    return data
