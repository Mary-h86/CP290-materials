"""Load and validate audit CSVs. Calculation code stays in the notebook."""
from pathlib import Path

import numpy as np
import pandas as pd

from audit_items import CODES, EXCLUDED, ITEM_SPECS

REQUIRED_COLUMNS = {
    "team", "route", "instrument", "unit", "item", "question", "rater", "mode",
    "value", "value_label", "code", "unit_minutes", "imagery", "capture_date", "unit_note",
}
IDENTITY_COLUMNS = ["route", "instrument", "unit", "item", "team", "rater", "mode"]
ISSUE_COLUMNS = ["team", "route", "instrument", "unit", "item", "rater", "mode", "value", "code", "issue"]
ITEM_KINDS = pd.Series({key: kind for key, (kind, _) in ITEM_SPECS.items()}, name="_kind")
ITEM_KINDS.index.names = ["instrument", "item"]
ALLOWED_ANSWERS = pd.MultiIndex.from_tuples(
    [(instrument, item, answer) for (instrument, item), (_, options) in ITEM_SPECS.items()
     for answer in options], names=["instrument", "item", "answer"],
)


def prepare_route_scores(frame, route):
    """Return one route's normalized scores and a separate table of invalid answers."""
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"The class file is missing columns: {sorted(missing)}")
    route = route.strip().upper()
    if route not in set(frame["route"]):
        raise ValueError(f'The file has no records for route "{route}". Routes in it: {sorted(frame.route.unique())}.')

    scores = frame.loc[frame["route"].eq(route)].drop_duplicates().reset_index(drop=True)
    if scores[["route", "team", "rater", "unit", "item"]].eq("").any().any():
        raise ValueError("A record is missing its route, team, rater, unit, or item.")
    if scores.duplicated(IDENTITY_COLUMNS).any():
        raise ValueError("Conflicting records for the same rater, unit, and item.")
    if not scores["mode"].isin(["field", "virtual"]).all():
        raise ValueError("Every record's mode must be field or virtual.")

    raw_items = scores["item"].copy()
    crossing_item = scores["instrument"].eq("MAPS") & scores["unit"].str.startswith("X") & ~scores["item"].str.startswith("X")
    scores.loc[crossing_item, "item"] = "X" + scores.loc[crossing_item, "item"]
    if scores.duplicated(IDENTITY_COLUMNS).any():
        raise ValueError("Conflicting records after normalizing MAPS crossing item IDs.")
    scores = scores.join(ITEM_KINDS, on=["instrument", "item"])

    # Validate whole columns, with one schema join and one numeric conversion.
    segment = scores["unit"].isin(["S1", "S2", "S3", "S4", "S5", "S6"])
    crossing = scores["unit"].str.fullmatch(r"X\d+")
    maps = scores["instrument"].eq("MAPS")
    actual_unit = np.select([segment, crossing], ["segment", "crossing"], default="route")
    expected_unit = np.select([scores["item"].str.startswith("X"), scores["item"].str.match(r"\d")],
                              ["crossing", "segment"], default="route")
    coded = scores["code"].ne("")
    answered = scores["value"].ne("")
    numeric = scores["_kind"].eq("number") & answered & ~coded
    number = pd.to_numeric(scores["value"], errors="coerce")
    numeric_text = scores["value"].str.strip().str.fullmatch(
        r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?|[+-]?(?:inf(?:inity)?|nan)", case=False,
    )
    valid_number = np.isfinite(number) & number.ge(0) & number.mod(1).eq(0)

    categorical = scores["_kind"].isin(["single", "scale", "multi"]) & answered & ~coded
    tokens = scores.loc[categorical, ["instrument", "item", "value", "_kind"]].rename(columns={"value": "answer"})
    multi = tokens["_kind"].eq("multi")
    tokens.loc[multi, "answer"] = tokens.loc[multi, "answer"].str.split("+")
    tokens = tokens.explode("answer")
    invalid_tokens = ~pd.MultiIndex.from_frame(tokens[["instrument", "item", "answer"]]).isin(ALLOWED_ANSWERS)
    invalid_answer = pd.Series(invalid_tokens, index=tokens.index).groupby(level=0).any().reindex(scores.index, fill_value=False)

    scores["issue"] = np.select(
        [scores["instrument"].eq("PEDS") & ~segment,
         maps & ~(segment | crossing | scores["unit"].eq("Route")),
         maps & (actual_unit != expected_unit), scores["_kind"].isna(),
         coded & ~scores["code"].isin(CODES), coded & answered,
         numeric & ~numeric_text, numeric & ~valid_number, invalid_answer],
        ["PEDS requires a segment unit S1–S6", "Unknown MAPS unit",
         "Question belongs to a different MAPS unit type", "Unknown instrument/item",
         "Unknown code", "Both a score and a code", "Expected a number",
         "Expected a nonnegative whole number", "Answer outside the form's response options"],
        default="",
    )
    issues = scores.loc[scores["issue"].ne(""), ISSUE_COLUMNS].copy()
    issues["item"] = raw_items.loc[issues.index]

    scores["score"] = scores["code"].where(coded, scores["value"])
    scores["key"] = scores["score"]
    valid = scores["issue"].eq("")
    # Only number formatting and set joining require scalar operations.
    scores.loc[numeric & valid, "key"] = number.loc[numeric & valid].map(lambda value: str(int(value)))
    parts = tokens.loc[tokens["_kind"].eq("multi") & valid.reindex(tokens.index)].reset_index(names="_row")
    canonical = (parts.sort_values(["_row", "answer"]).drop_duplicates(["_row", "answer"])
                 .groupby("_row", sort=False)["answer"].agg("+".join))
    scores.loc[canonical.index, "key"] = canonical
    scores.loc[~valid, "key"] = "INVALID"
    scores["value_label"] = scores["value_label"].where(scores["value_label"].ne(""), scores["value"])
    scores["who"] = "T" + scores["team"] + "-" + scores["rater"]
    included = ~pd.MultiIndex.from_frame(scores[["instrument", "item"]]).isin(EXCLUDED)
    return scores.loc[included].drop(columns="_kind"), issues


def load_route_scores(path, route):
    """Read the supplied local CSV; strings such as 'None' remain answers."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Place {path.name} beside the notebook.")
    return prepare_route_scores(pd.read_csv(path, dtype=str, keep_default_na=False), route)
