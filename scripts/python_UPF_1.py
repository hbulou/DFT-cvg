import xml.etree.ElementTree as ET

def read_upf(file_path):
    """
    Lit un fichier UPF au format XML et retourne son contenu sous forme de dictionnaire.
    
    :param file_path: Chemin vers le fichier UPF.
    :return: Dictionnaire contenant les informations principales.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Extraire des informations utiles
        upf_data = {
            "element": root.findtext('PP_HEADER/ELEMENT'),
            "z_valence": root.findtext('PP_HEADER/Z_VALENCE'),
            "l_max": root.findtext('PP_HEADER/L_MAX'),
            "cutoff": root.findtext('PP_INFO/CUTOFF'),
        }
        return upf_data
    except ET.ParseError:
        print("Erreur de parsing : Le fichier UPF ne semble pas être au format XML valide.")
        return None
    except FileNotFoundError:
        print("Erreur : Le fichier spécifié n'existe pas.")
        return None

# Exemple d'utilisation
upf_file = "path/to/your/file.upf"  # Remplacez par le chemin réel
upf_content = read_upf(upf_file)

if upf_content:
    print("Données extraites du fichier UPF :")
    for key, value in upf_content.items():
        print(f"{key}: {value}")

