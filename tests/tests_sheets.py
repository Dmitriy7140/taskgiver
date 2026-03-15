from sheets import Sheets

def test_returns_not_used_link():
    sheets = Sheets.__new__(Sheets)
    sheets.links = ["a", "b", "c"]
    used_links = ["c"]

    assert sheets.get_random_link(used_links) not in used_links
def test_returns_empty_list_if_no_links_available():
    sheets = Sheets.__new__(Sheets)
    sheets.links = ["a", "b", "c"]
    used_links = ["a", "b", "c"]

    assert sheets.get_random_link(used_links) == []