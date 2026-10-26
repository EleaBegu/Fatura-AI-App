from database import SessionLocal, engine
import models

# Sigurohemi që tabelat ekzistojnë
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Artikujt realë të marrë nga skedari "Lista e produkteve.xlsx"
produktet_reale = [
    # Shtrafa & Vida
    {"kodi": "STR-001", "emri": "SHRAFA MEKANIZMI 4.1x25", "kategoria": "Shtrafa", "njesia": "Pack(1000copë)", "cmimi": 12.50},
    {"kodi": "STR-002", "emri": "SHRAFA PER BAGLLAME 4.1x35", "kategoria": "Shtrafa", "njesia": "Pack(1000copë)", "cmimi": 14.00},
    {"kodi": "STR-003", "emri": "SHRAFA VETESHPUES 3.9x16", "kategoria": "Shtrafa", "njesia": "Pack(1000copë)", "cmimi": 9.50},
    {"kodi": "STR-004", "emri": "SHRAFA VETESHPUES 3.9x19", "kategoria": "Shtrafa", "njesia": "Pack(1000copë)", "cmimi": 10.00},
    {"kodi": "STR-005", "emri": "SHRAFA VETESHPUES 3.9x32", "kategoria": "Shtrafa", "njesia": "Pack(1000copë)", "cmimi": 11.80},
    {"kodi": "STR-006", "emri": "SHRAFA MONTIMI 7.5x132", "kategoria": "Shtrafa Montimi", "njesia": "Copë", "cmimi": 0.15},
    {"kodi": "STR-007", "emri": "SHRAFA MONTIMI 7.5x182", "kategoria": "Shtrafa Montimi", "njesia": "Copë", "cmimi": 0.22},
    {"kodi": "VID-001", "emri": "VIDA PER PVC 3.9X25", "kategoria": "Vida PVC", "njesia": "Pack(1000copë)", "cmimi": 10.50},
    {"kodi": "VID-002", "emri": "VIDA PER PVC 3.9X35", "kategoria": "Vida PVC", "njesia": "Pack(1000copë)", "cmimi": 12.00},
    
    # Vegla & Burgi
    {"kodi": "BRG-001", "emri": "BURGI METALI 3mm", "kategoria": "Vegla/Burgi", "njesia": "Copë", "cmimi": 0.80},
    {"kodi": "BRG-002", "emri": "BURGI METALI 5mm", "kategoria": "Vegla/Burgi", "njesia": "Copë", "cmimi": 1.20},
    {"kodi": "BRG-003", "emri": "BURGI METALI 7mm", "kategoria": "Vegla/Burgi", "njesia": "Copë", "cmimi": 1.80},
    {"kodi": "BRG-004", "emri": "BURGI BETONI 6x210", "kategoria": "Vegla/Burgi", "njesia": "Copë", "cmimi": 2.50},
    
    # Materiale pune & Aksesorë
    {"kodi": "AKS-001", "emri": "SHRAFA ROLETASH 582", "kategoria": "Aksesorë", "njesia": "Copë", "cmimi": 0.05},
    {"kodi": "AKS-002", "emri": "DOREZA BALLKONI ALU", "kategoria": "Aksesorë", "njesia": "Copë", "cmimi": 3.50},
    {"kodi": "AKS-003", "emri": "KAPAKA AMO ngj.bardhë", "kategoria": "Aksesorë", "njesia": "Copë", "cmimi": 0.20},
    {"kodi": "MAT-001", "emri": "KLEBFIX", "kategoria": "Kimikate/Ngjitës", "njesia": "Copë", "cmimi": 4.50},
    {"kodi": "MAT-002", "emri": "TEFLON SPRAY", "kategoria": "Kimikate/Ngjitës", "njesia": "Copë", "cmimi": 3.80},
]

print("Po fusim të dhënat reale në bazën e të dhënave...")

for p in produktet_reale:
    # Kontrollojmë nëse produkti ekziston që të mos përsëritet
    ekziston = db.query(models.Produkti).filter(models.Produkti.kodi == p["kodi"]).first()
    if not ekziston:
        db.add(models.Produkti(
            kodi=p["kodi"],
            emri=p["emri"],
            kategoria=p["kategoria"],
            njesia=p["njesia"],
            cmimi=p["cmimi"]
        ))

db.commit()

# Fatura testuese nga firma e babait
fatura_test = db.query(models.Fatura).filter(models.Fatura.nr_fatures == "FAT-2024-001").first()
if not fatura_test:
    fatura_nova = models.Fatura(
        nr_fatures="FAT-2024-001",
        furnizuesi="WINAKS SH.P.K.",
        shuma_totale=158.40,
        tvsh=28.51,
        data_fatures="2024-05-15"
    )
    db.add(fatura_nova)
    db.commit()

    # Rreshtat e faturës
    rreshtat = [
        models.RreshtiFatures(fatura_id=fatura_nova.id, pershkrimi="SHRAFA MEKANIZMI 4.1x25", sasia=10, cmimi_njesi=12.50, nentotali=125.00),
        models.RreshtiFatures(fatura_id=fatura_nova.id, pershkrimi="DOREZA BALLKONI ALU", sasia=6, cmimi_njesi=3.50, nentotali=21.00),
    ]
    for r in rreshtat:
        db.add(r)
    db.commit()

db.close()
print("Sukses! Të gjitha të dhënat nga skedari i firmës u shtuan në bazën e të dhënave.")
