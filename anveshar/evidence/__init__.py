"""Anveshar evidence connectors.

Thin, best effort adapters over public biomedical evidence sources (NCBI
E-utilities for PubMed and ClinVar, ClinicalTrials.gov API v2, and a set of
molecular workbench REST endpoints). Every network call uses a short timeout
and degrades to an empty result (empty list or empty dict) on any failure, so
callers can rely on a stable return shape without handling exceptions.

Each module exposes a pure parse function (``_parse_esummary``,
``_parse_studies``, ``_parse_clinvar``) that turns a raw JSON payload into the
canonical shape without touching the network, so behavior can be unit tested
offline.
"""
from . import pubmed, clinicaltrials, clinvar, workbench
from .workbench import WorkbenchClient

__all__ = ["pubmed", "clinicaltrials", "clinvar", "workbench", "WorkbenchClient"]
