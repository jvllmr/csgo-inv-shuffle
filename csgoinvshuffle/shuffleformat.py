# flake8: noqa


HEADER = '"SavedItemShuffles"\n{\n'
INDENT = "\t"
ENABLED_INDENT = INDENT + INDENT
ITEM_INDENT = " " + INDENT
ITEM_ENTRY_INDENT = ENABLED_INDENT + INDENT
END = "}"
ITEM_ENTRY = ITEM_ENTRY_INDENT + '"$nr$"' + ITEM_INDENT + '"$item_id$"\n'
SLOT_ENTRY = (
    INDENT
    + '"$id$"\n'
    + INDENT
    + "{\n"
    + ENABLED_INDENT
    + '"enabled"'
    + ENABLED_INDENT
    + '"1"\n'
    + ENABLED_INDENT
    + '"items"\n'
    + ENABLED_INDENT
    + "{\n$item_entries$"
    + ENABLED_INDENT
    + "}\n"
    + INDENT
    + "}\n"
)
