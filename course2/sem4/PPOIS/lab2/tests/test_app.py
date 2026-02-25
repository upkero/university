from __future__ import annotations

import tempfile
import unittest
from datetime import date
from pathlib import Path

from src.app.model import Player, PlayerRepository, SearchQuery
from src.app.xml_storage import load_players_sax, save_players_dom


def sample_players() -> list[Player]:
    return [
        Player("Ivanov", "Pavel", "Sergeevich", date(1998, 5, 4), "Dynamo Minsk", "Minsk", "Main", "Goalkeeper"),
        Player("Petrov", "Andrey", "Ilyich", date(2001, 7, 12), "BATE", "Borisov", "Reserve", "Defender"),
        Player("Sidorov", "Nikita", "Olegovich", date(1999, 1, 20), "Shakhtar Soligorsk", "Soligorsk", "Main", "Forward"),
    ]


class SearchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = PlayerRepository(sample_players())

    def test_fio_date(self) -> None:
        query = SearchQuery(first_name="Pavel", birth_date=date(1998, 5, 4))
        found = self.repo.search(query)
        self.assertEqual(1, len(found))
        self.assertEqual("Ivanov", found[0].last_name)

    def test_position_or_squad(self) -> None:
        query = SearchQuery(position="Defender", squad="Main")
        found = self.repo.search(query)
        self.assertEqual(3, len(found))

    def test_team_or_city(self) -> None:
        query = SearchQuery(team="BATE", home_city="Soligorsk")
        found = self.repo.search(query)
        self.assertEqual(2, len(found))

    def test_validate_only_one_fio_part(self) -> None:
        query = SearchQuery(last_name="Ivanov", first_name="Pavel")
        with self.assertRaises(ValueError):
            query.validate(require_non_empty=True)

    def test_delete(self) -> None:
        query = SearchQuery(squad="Reserve")
        query.validate(require_non_empty=True)
        deleted = self.repo.delete(query)
        self.assertEqual(1, deleted)
        self.assertEqual(2, len(self.repo.all()))

    def test_fio_output_normalized_to_title_case(self) -> None:
        player = Player("iVAnOv", "pAveL", "sErGeEvIch", date(2000, 1, 1), "Team", "City", "S", "P")
        self.assertEqual("Ivanov Pavel Sergeevich", player.full_name)

    def test_search_is_case_insensitive(self) -> None:
        query = SearchQuery(first_name="pAvEL")
        found = self.repo.search(query)
        self.assertEqual(1, len(found))

    def test_invalid_fio_symbols_in_query(self) -> None:
        query = SearchQuery(first_name="Pavel1")
        with self.assertRaises(ValueError):
            query.validate(require_non_empty=False)

    def test_invalid_fio_symbols_in_player(self) -> None:
        with self.assertRaises(ValueError):
            Player("Ivanov-", "Pavel", "", date(2000, 1, 1), "Team", "City", "S", "P")


class XmlTests(unittest.TestCase):
    def test_dom_save_sax_load(self) -> None:
        players = sample_players()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "players.xml"
            save_players_dom(players, path)
            loaded = load_players_sax(path)
        self.assertEqual(len(players), len(loaded))
        self.assertEqual(players[0].birth_date, loaded[0].birth_date)
        self.assertEqual(players[1].team, loaded[1].team)

    def test_sax_load_cp1251_without_decl(self) -> None:
        xml_text = """
<players>
  <player>
    <last_name>ИВАНОВ</last_name>
    <first_name>ПАВЕЛ</first_name>
    <middle_name>СЕРГЕЕВИЧ</middle_name>
    <birth_date>1998-05-04</birth_date>
    <team>Динамо Минск</team>
    <home_city>Минск</home_city>
    <squad>Основной</squad>
    <position>Вратарь</position>
  </player>
</players>
""".strip()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cp1251.xml"
            path.write_bytes(xml_text.encode("cp1251"))
            loaded = load_players_sax(path)
        self.assertEqual(1, len(loaded))
        self.assertEqual("Иванов", loaded[0].last_name)
        self.assertEqual("Павел", loaded[0].first_name)


if __name__ == "__main__":
    unittest.main()
