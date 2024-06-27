from pony import orm
 
# připrav spojení na databázi a vytvoř databázový soubor na disku
db = orm.Database()
db.bind(provider='sqlite', filename='izotopy.db', create_db=True)

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

# propojení tabulky v databázi na objekty v Pythonu
db.generate_mapping(create_tables=True)

#
# naplnění tabulek daty
#
with orm.db_session:

    # A) tabulka izotopů
    with open('nuclear-wallet-cards_2011.csv') as f:
        next(f)     # hlavičku přeskakuji
        for řádka in f:
            F, A, M, Z, element, J, decay_mode, branch, excitation_energy, Q, T, abundance, atomic_mass, delta_mass, S, date, Ts = řádka.rstrip().split(';')
            Isotopes(
                F=F,
                A=A,
                M=M,
                Z=Z,
                element=element,
                J=J,
                decay_mode=decay_mode,
                branch=branch,
                excitation_energy=excitation_energy,
                Q=Q,
                T=T,
                abundance=abundance,
                atomic_mass=atomic_mass,
                delta_mass=delta_mass,
                S=S,
                date=date,
                Ts=Ts
            )

    # B) tabulka prvků
    with open('elements-from-wiki.csv', encoding='utf-8') as f:
        next(f)     # hlavičku přeskakuji
        for řádka in f:
            Z, symbol, name, origin_of_name, group, period, block, Ar, density, melting_point, boiling_point, Cp, X, abudance, origin, phase = řádka.rstrip().split('\t')
            Z, symbol, name, origin_of_name, group, period, block, Ar, density, melting_point, boiling_point, Cp, X, abudance, origin, phase = Z.strip(), symbol.strip(), name.strip(), origin_of_name.strip(), group.strip(), period.strip(), block.strip(), Ar.strip(), density.strip(), melting_point.strip(), boiling_point.strip(), Cp.strip(), X.strip(), abudance.strip(), origin.strip(), phase.strip()
            Elements(
                Z=Z,
                symbol=symbol,
                name=name,
                origin_of_name=origin_of_name,
                group=group,
                period=period,
                block=block,
                Ar=Ar,
                density=density,
                melting_point=melting_point,
                boiling_point=boiling_point,
                Cp=Cp,
                X=X,
                abudance=abudance,
                origin=origin,
                phase=phase
            )
