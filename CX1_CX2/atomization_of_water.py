from ase.build import molecule
from gpaw import GPAW
from ase.parallel import paropen

a = 8.0
h = 0.2


energies = {}
with paropen('paropenresults-%.2f.txt' % h, 'w') as resultfile:

    for name in ['H2O', 'H', 'O']:
        system = molecule(name)
        system.set_cell((a, a, a))
        system.center()
    
        calc = GPAW(h=h,
                    txt=f'gpaw-{name}-{h:.2f}.txt')
        if name == 'H' or name == 'O':
            calc.set(hund=True)
    
        system.calc = calc
    
        energy = system.get_potential_energy()
        energies[name] = energy
        print(name, energy, file=resultfile)
    
    e_atomization = energies['H2O'] - 2 * energies['H'] - energies['O']
    print(e_atomization, file=resultfile)