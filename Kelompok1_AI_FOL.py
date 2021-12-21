from logic import *

class FolKB(KB):
  def __init__(self, initial_clauses=[]):
   self.clauses = []  # inefficient: no indexing
   for clause in initial_clauses:
    self.tell(clause)

  def tell(self, sentence):
   if is_definite_clause(sentence):
    self.clauses.append(sentence)
   else:
    raise Exception("Not a definite clause: {}".format(sentence))

  def ask_generator(self, query):
   q = expr(query)
   test_variables = variables(q)
   answers = fol_bc_ask(self, q)
   return sorted([dict((x, v) for x, v in list(a.items())
                       if x in test_variables)
                  for a in answers], key=repr)

  def retract(self, sentence):
   self.clauses.remove(sentence)

  def fetch_rules_for_goal(self, goal):
   return self.clauses

symptoms_kb = FolKB(
    map(expr,
           [
            'Diagnosa1(g1,g2,g3,g4,penyakit) ==> Gejala(g1,g2,g3,g4,penyakit)',
            'Diagnosa1(Y,g2,g3,g4,DBD)',
            'Diagnosa2(N,g2,g3,g4,penyakit) ==> Diagnosa1(N,g2,g3,g4,penyakit)',
            'Diagnosa2(N,N,g3,g4,TidakDBD)',
            'Diagnosa3(N,Y,g3,g4,penyakit) ==> Diagnosa2(N,Y,g3,g4,penyakit)',
            'Diagnosa3(N,Y,Y,g4,DBD)',
            'Diagnosa4(N,Y,N,g4,penyakit) ==> Diagnosa3(N,Y,N,g4,penyakit)',
            'Diagnosa4(N,Y,N,Y,DBD)', 'Diagnosa4(N,Y,N,N,TidakDBD)'
           ]
        ),
)
print("\ngejala-gejalanya :\n")
print("g1 : Rasa besi dimulut \t\t(Y atau N)")
print("g2 : Mual dan muntah \t\t\t\t(Y atau N)")
print("g3 : Sakit dibagian perut \t\t(Y atau N)")
print("g4 : Nyeri tulang sendi \t\t\t\t(Y atau N)")

print("\ncontoh inputnya :")
print('Gejala(N,N,N,N,penyakit)')
print("\ncontoh output :")
print(repr(symptoms_kb.ask_generator('Gejala(N,N,N,N,penyakit)')))

print("\noutput :")


ask = repr(symptoms_kb.ask_generator('Gejala(N,Y,N,Y,penyakit)'))
if (ask == "[]"):
    print("Input anda salah atau diagnosa penyakit diluar DBD")
else :
    print(ask)

