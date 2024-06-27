from pony import orm
 
# připrav spojení na databázi a vytvoř databázový soubor na disku
db = orm.Database()

# 
# příprava tabulek
# 


# A) tabulka izotopů
class Isotopes(db.Entity):
    F = orm.Optional(str)
    A = orm.Optional(str)
    M = orm.Optional(str)
    Z = orm.Optional(str)
    element = orm.Optional(str)
    J = orm.Optional(str)
    decay_mode = orm.Optional(str)
    branch = orm.Optional(str)
    excitation_energy = orm.Optional(str)
    Q = orm.Optional(str)
    T = orm.Optional(str)
    abundance = orm.Optional(str)
    atomic_mass = orm.Optional(str)
    delta_mass = orm.Optional(str)
    S = orm.Optional(str)
    date = orm.Optional(str)
    Ts = orm.Optional(str)


# B) tabulka prvků
class Elements(db.Entity):
    Z = orm.Optional(str)
    symbol = orm.Optional(str)
    name = orm.Optional(str)
    origin_of_name = orm.Optional(str)
    group = orm.Optional(str)
    period = orm.Optional(str)
    block = orm.Optional(str)
    Ar = orm.Optional(str)
    density = orm.Optional(str)
    melting_point = orm.Optional(str)
    boiling_point = orm.Optional(str)
    Cp = orm.Optional(str)
    X = orm.Optional(str)
    abudance = orm.Optional(str)
    origin = orm.Optional(str)
    phase = orm.Optional(str)

    def identify(self):
        return f'{self.name} ({self.symbol}) --> group {self.group} | period {self.period} | block {self.block}'
