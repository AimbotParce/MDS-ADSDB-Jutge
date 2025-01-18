from yogi import scan


class GossipManager:
    def __init__(self):
        self.couples: dict[str, str] = dict()
        self.alone: set[str] = set()

    def __str__(self):
        res = "COUPLES:"
        for p1, p2 in sorted(self.couples.items()):
            if p1 < p2:
                res += f"\n{p1} {p2}"
        res += "\nALONE:"
        for p in sorted(self.alone):
            res += f"\n{p}"
        return res

    def addAffair(self, p1: str, p2: str) -> None:
        self.alone.discard(p1)
        self.alone.discard(p2)
        p1_partner = self.couples.get(p1)
        if p1_partner is not None:
            del self.couples[p1_partner]
            self.alone.add(p1_partner)
        p2_partner = self.couples.get(p2)
        if p2_partner is not None:
            del self.couples[p2_partner]
            self.alone.add(p2_partner)
        self.couples[p1] = p2
        self.couples[p2] = p1


if __name__ == "__main__":
    gossip = GossipManager()
    while (ord := scan(str)) is not None:
        if ord == "info":
            print(gossip)
            print("-" * 10)
        elif ord == "affair":
            p1 = scan(str)
            p2 = scan(str)
            gossip.addAffair(p1, p2)
        else:
            raise ValueError(f"Unknown command: {ord}")
