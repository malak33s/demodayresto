from db_connection import session, TableExample

# Ajouter une entrée
nouvelle_entree = TableExample(name="TestName")
session.add(nouvelle_entree)
session.commit()

# Vérifier que l'entrée a bien été ajoutée
resultat = session.query(TableExample).filter_by(name="TestName").first()

if resultat:
    print(f"✅ Entrée ajoutée avec succès : {resultat.name}")
else:
    print("⚠️ Problème lors de l'ajout de l'entrée.")

session.close()
