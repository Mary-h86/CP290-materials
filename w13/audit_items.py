"""Item definitions and answer validation for the audit entry forms."""
import math

CODES = {"NC", "NV", "VT"}
UNUSABLE = CODES | {"INVALID"}
SEPARATE = {("MAPS", "15a"), ("MAPS", "15b"), ("MAPS", "15c")}
EXCLUDED = SEPARATE | {("MAPS", "L1")}  # collection method is metadata
NUMERIC = {
    ("PEDS", "B13"), ("PEDS", "C15a"), ("PEDS", "C15b"), ("PEDS", "C16b"),
    ("PEDS", "SA1"), ("PEDS", "SA2"), ("PEDS", "SA3"), ("PEDS", "SA4"),
    ("MAPS", "6"), ("MAPS", "S1a"), ("MAPS", "S1b"), ("MAPS", "S3a"), ("MAPS", "S3b"),
}

# BEGIN ITEM SPECS
ITEM_SPECS = {
    ('PEDS', '0'): ('single', ('1', '2', '3')),
    ('PEDS', 'A1'): ('multi', ('1', '2', '3', '4', '5', '6', '7', '8')),
    ('PEDS', 'A2'): ('single', ('1', '2', '3')),
    ('PEDS', 'A3'): ('multi', ('1', '2', '3', '4', '5', '6')),
    ('PEDS', 'B4'): ('multi', ('1', '2', '3', '4')),
    ('PEDS', 'B5'): ('multi', ('1', '2', '3', '4', '5')),
    ('PEDS', 'B6'): ('single', ('1', '2', '3', '4')),
    ('PEDS', 'B7'): ('multi', ('1', '2', '3', '4', '5', '6')),
    ('PEDS', 'B8'): ('multi', ('1', '2', '3', '4', '5', '6')),
    ('PEDS', 'B9'): ('single', ('1', '2', '3')),
    ('PEDS', 'B10'): ('single', ('1', '2', '3')),
    ('PEDS', 'B11'): ('single', ('1', '2', '3')),
    ('PEDS', 'B12'): ('single', ('1', '2')),
    ('PEDS', 'B13'): ('number', ()),
    ('PEDS', 'C14'): ('single', ('1', '2', '3', '4')),
    ('PEDS', 'C15a'): ('number', ()),
    ('PEDS', 'C15b'): ('number', ()),
    ('PEDS', 'C16a'): ('single', ('1', '2')),
    ('PEDS', 'C16b'): ('number', ()),
    ('PEDS', 'C17'): ('single', ('1', '2')),
    ('PEDS', 'C18'): ('single', ('1', '2', '3')),
    ('PEDS', 'C19'): ('single', ('1', '2')),
    ('PEDS', 'C20'): ('single', ('1', '2', '3')),
    ('PEDS', 'C21'): ('multi', ('1', '2', '3', '4', '5', '6')),
    ('PEDS', 'C22'): ('single', ('1', '2', '3', '4')),
    ('PEDS', 'C23'): ('multi', ('1', '2', '3', '4', '5', '6', '7', '8', '9')),
    ('PEDS', 'C24'): ('multi', ('1', '2', '3', '4', '5')),
    ('PEDS', 'D25'): ('single', ('1', '2', '3', '4')),
    ('PEDS', 'D26'): ('multi', ('1', '2', '3', '4', '5')),
    ('PEDS', 'D27'): ('single', ('1', '2')),
    ('PEDS', 'D28'): ('single', ('1', '2', '3')),
    ('PEDS', 'D29'): ('single', ('1', '2', '3')),
    ('PEDS', 'D30'): ('single', ('1', '2', '3')),
    ('PEDS', 'D31'): ('single', ('1', '2', '3')),
    ('PEDS', 'D32'): ('single', ('1', '2', '3')),
    ('PEDS', 'D33'): ('single', ('1', '2', '3')),
    ('PEDS', 'D34'): ('single', ('1', '2', '3')),
    ('PEDS', 'D35'): ('single', ('1', '2', '3', '4')),
    ('PEDS', 'SA1'): ('scale', ('1', '2', '3', '4')),
    ('PEDS', 'SA2'): ('scale', ('1', '2', '3', '4')),
    ('PEDS', 'SA3'): ('scale', ('1', '2', '3', '4')),
    ('PEDS', 'SA4'): ('scale', ('1', '2', '3', '4')),
    ('MAPS', 'L1'): ('single', ('1', '2', '3', '4')),
    ('MAPS', 'L2'): ('multi', ('1', '2', '3', '4', '5')),
    ('MAPS', 'L3a'): ('single', ('1', '2', '3')),
    ('MAPS', 'L3b'): ('single', ('1', '2', '3')),
    ('MAPS', 'L3c'): ('single', ('1', '2', '3')),
    ('MAPS', 'L3d'): ('single', ('1', '2', '3')),
    ('MAPS', 'L3e'): ('single', ('1', '2', '3')),
    ('MAPS', 'L3f'): ('single', ('1', '2', '3')),
    ('MAPS', 'L3g'): ('single', ('1', '2', '3')),
    ('MAPS', 'L3h'): ('single', ('1', '2', '3')),
    ('MAPS', 'L3i'): ('single', ('1', '2', '3')),
    ('MAPS', 'L3j'): ('single', ('1', '2', '3')),
    ('MAPS', 'L3k'): ('single', ('1', '2', '3')),
    ('MAPS', 'L3l'): ('single', ('1', '2', '3')),
    ('MAPS', 'L3m'): ('single', ('1', '2', '3')),
    ('MAPS', 'L3n'): ('single', ('1', '2', '3')),
    ('MAPS', 'L3o'): ('single', ('1', '2', '3')),
    ('MAPS', 'S1a'): ('number', ()),
    ('MAPS', 'S1b'): ('number', ()),
    ('MAPS', 'S2'): ('multi', ('1', '2', '3')),
    ('MAPS', 'S3a'): ('number', ()),
    ('MAPS', 'S3b'): ('number', ()),
    ('MAPS', 'S4'): ('single', ('1', '2', '3')),
    ('MAPS', 'S5'): ('single', ('1', '2', '3', '4')),
    ('MAPS', 'S6'): ('multi', ('1', '2', '3', '4')),
    ('MAPS', 'AS1'): ('single', ('1', '2')),
    ('MAPS', 'AS2'): ('single', ('1', '2')),
    ('MAPS', 'AS3'): ('single', ('1', '2', '3', '4')),
    ('MAPS', 'AS4'): ('single', ('1', '2', '3', '4')),
    ('MAPS', 'AS5'): ('single', ('1', '2')),
    ('MAPS', 'AS6'): ('single', ('1', '2', '3', '4')),
    ('MAPS', 'AS7'): ('single', ('1', '2')),
    ('MAPS', '1'): ('single', ('1', '2')),
    ('MAPS', '2'): ('single', ('1', '2', '3', '4')),
    ('MAPS', '3'): ('single', ('1', '2')),
    ('MAPS', '4'): ('single', ('1', '2', '3')),
    ('MAPS', '5'): ('single', ('1', '2', '3', '4', '5')),
    ('MAPS', '6'): ('single', ('0', '1', '2', '3', '4', '5', '6', '7')),
    ('MAPS', '7'): ('single', ('1', '2')),
    ('MAPS', '8'): ('single', ('1', '2')),
    ('MAPS', '9'): ('single', ('1', '2', '3', '4', '5', '6')),
    ('MAPS', '10'): ('single', ('1', '2', '3')),
    ('MAPS', '11'): ('single', ('1', '2', '3', '4', '5', '6')),
    ('MAPS', '12'): ('single', ('1', '2', '3', '4', '5', '6')),
    ('MAPS', '13'): ('single', ('1', '2', '3', '4', '5', '6')),
    ('MAPS', '14'): ('single', ('1', '2', '3', '4', '5')),
    ('MAPS', '15a'): ('number', ()),
    ('MAPS', '15b'): ('single', ('1', '2', '3', '4')),
    ('MAPS', '15c'): ('single', ('1', '2', '3')),
    ('MAPS', 'X1'): ('single', ('1', '2')),
    ('MAPS', 'X2'): ('multi', ('1', '2', '3', '4')),
    ('MAPS', 'X3a'): ('single', ('1', '2', '3')),
    ('MAPS', 'X3b'): ('single', ('1', '2', '3')),
    ('MAPS', 'X4'): ('single', ('1', '2')),
    ('MAPS', 'X5'): ('multi', ('1', '2', '3', '4')),
    ('MAPS', 'X6'): ('single', ('1', '2')),
}
# END ITEM SPECS


def item_key(row):
    """Keep MAPS crossing and segment questions with the same number separate."""
    item = row["item"]
    if row["instrument"] == "MAPS" and row["unit"].startswith("X") and not item.startswith("X"):
        return "X" + item
    return item


def score_issue(row):
    """Validate an answer against the entry form without changing the raw record."""
    unit = row["unit"]
    segment = unit in {"S1", "S2", "S3", "S4", "S5", "S6"}
    crossing = unit.startswith("X") and unit[1:].isdigit()
    if row["instrument"] == "PEDS" and not segment:
        return "PEDS requires a segment unit S1–S6"
    if row["instrument"] == "MAPS":
        item = item_key(row)
        if not (segment or crossing or unit == "Route"):
            return "Unknown MAPS unit"
        expected = "crossing" if item.startswith("X") else ("segment" if item[:1].isdigit() else "route")
        if expected != ("segment" if segment else "crossing" if crossing else "route"):
            return "Question belongs to a different MAPS unit type"
    spec = ITEM_SPECS.get((row["instrument"], item_key(row)))
    if spec is None:
        return "Unknown instrument/item"
    code, value = row.get("code", ""), row.get("value", "")
    if code:
        if code not in CODES:
            return "Unknown code"
        return "Both a score and a code" if value else ""
    if not value:
        return ""
    kind, options = spec
    if kind == "number":
        try:
            n = float(value)
        except ValueError:
            return "Expected a number"
        return "" if math.isfinite(n) and n >= 0 and n.is_integer() else "Expected a nonnegative whole number"
    answers = value.split("+") if kind == "multi" else [value]
    return "" if all(a in options for a in answers) else "Answer outside the form's response options"


def score_key(row):
    """Canonical comparison key; invalid answers cannot agree with each other."""
    if score_issue(row):
        return "INVALID"
    if row.get("code"):
        return row["code"]
    value = row.get("value", "")
    if value and ITEM_SPECS[(row["instrument"], item_key(row))][0] == "number":
        return str(int(float(value)))
    return "+".join(sorted(set(value.split("+"))))
