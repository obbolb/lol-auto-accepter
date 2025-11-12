from __future__ import annotations
from data.get_game_constants import get_champ_id


class ChampSelect:
    def __init__(
        self, client: LeagueClient, *, mode=None, pick=None, ban=None, rune=None
    ):  # pyright: ignore[reportUndefinedVariable]
        self.client = client
        self.mode = mode
        self.pick = pick
        self.ban = ban
        self.rune = rune

    def ban_pick(self):
        match self.mode:
            case "blind pick":
                self.client.requests(
                    "POST",
                )
            case "draft pick":

                pass
