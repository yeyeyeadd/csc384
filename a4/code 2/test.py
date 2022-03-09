from bnetbase import *
from medicalDiagnosis import *

def main():
    bmi.set_evidence("~18.5")

    co.set_evidence("NO")

    ht.set_evidence("NO")

    hl.set_evidence("NO")

    ag.set_evidence("<40")

    a = VE(medical, ac, [bmi])
    b = VE(medical, ac, [bmi, co])
    c = VE(medical, ac, [bmi, co, ht])
    d = VE(medical, ac, [bmi, co, ht, hl])
    e = VE(medical, ac, [bmi, co, ht, hl, ag])

    print(a)
    print(b)
    print(c)
    print(d)
    print(e)

if __name__ == '__main__':
    main()
