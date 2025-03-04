def read_upf_v1(file_path):
    """
    Lit un fichier UPF au format texte brut (v1.x).
    """
    data = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if "element" in line.lower():
                    data["element"] = line.split('=')[-1].strip()
                if "z_valence" in line.lower():
                    data["z_valence"] = line.split('=')[-1].strip()
    except FileNotFoundError:
        print("Erreur : Le fichier spécifié n'existe pas.")
    return data

