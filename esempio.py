class Pallone:
    CIRCONFERENZA = 50
    PESO = 1

    def __init__(self, nome_pallone, colore_pallone):
        self.nome: str = nome_pallone
        self.colore: str = colore_pallone
        self.is_signed: bool = False

    def get_nome(self) -> str:
        return self.nome

    def set_nome(self, nuovo_nome):
        self.nome = nuovo_nome


class PalloneA5(Pallone):
    CIRCONFERENZA = 20

    @staticmethod
    def gonfia_palloncino():
        return "gonfiato"


# codice vero
pallone_adidas = Pallone("adidas", "giallo")
print(pallone_adidas.get_nome())
pallone_adidas.set_nome("adidas - plus in cul")
print(pallone_adidas.get_nome())
pallone_puma = Pallone("puma", "verde")
palloncino_adidas = PalloneA5("adidas mini", "giallo")
palloncino_adidas.set_nome()
PalloneA5.gonfia_palloncino()
print("")
