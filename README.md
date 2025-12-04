📦 Quantum Data Engine — Python Simulation Framework

Quantum Data Engine je edukativni i eksperimentalni Python projekt koji simulira:

kvantne čvorove (amplituda, energija, superpozicija)

graf koji povezuje čvorove (entanglement, decoherence)

pretraživački engine (amplitude, energija, kombinirani filteri)

mehanizam spregnutosti (kvantna korelacija)

vizualni prikaz grafa (NetworkX + matplotlib)

animirani prikaz oscilacije amplitude

jednostavan storage layer (hashing, snapshot, WAL log)

Projekt je zamišljen kao mini–kvantna simulacija + mini–baza podataka, u čistom Pythonu, pogodna za učenje struktura podataka, algoritama i OOP arhitekture.

🚀 Pokretanje
1. Kreiraj virtual environment
python -m venv venv

2. Aktiviraj ga

Windows PowerShell:

.\venv\Scripts\activate

3. Instaliraj dependency-je
pip install -r requirements.txt

4. Pokreni engine
python main.py

🧠 Funkcionalnosti
✔️ Quantum čvorovi

amplitude

energija

veze (linkovi)

superpozicija

kolaps

✔️ Quantum Graph

spajanje čvorova

odstranjivanje “mrtvih” čvorova

decoherence (pad amplitude kroz vrijeme)

stabilizacija

✔️ SearchEngine

pretraga po amplitudi

pretraga po energiji

pretraga po vrijednosti

kombinirani filteri

rangiranje

✔️ Vizualizacija

statički graf (NetworkX)

animirana oscilacija amplitude

🔧 Storage layer

WAL log (write-ahead logging)

snapshot sistem

hashiranje stanja

Ovaj modul simulira osnovne principe baza podataka.

🧩 Struktura projekta
quantum_data_engine/
│
├── engine/
│   ├── node.py
│   ├── graph.py
│   ├── quantum_ops.py
│   └── stabilizer.py
│
├── storage/
│   ├── wal.py
│   ├── snapshot.py
│   ├── search_engine.py
│   └── indexer.py
│
├── visuals/
│   └── visualizer.py
│
├── utils/
│   └── hashing.py
│
├── main.py
├── README.md
└── requirements.txt

📜 Licenca

Projekt je objavljen pod MIT licencom, što znači da ga svako može koristiti, učiti iz njega i proširivati.

📚 Cilj projekta

Ovaj projekt služi kao:

trening iz Python OOP arhitekture

realistična simulacija grafova i dinamičkih sistema

uvod u kvantne algoritme (na jednostavnom nivou)

demonstracija rada baza podataka (WAL + snapshot)

Idealno za junior developere, studente i sve koji žele pokazati kompleksniji Python rad u portfolio-u.