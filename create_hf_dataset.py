# import pickle
# import pandas as pd
import os
# from PIL import Image
# from tqdm.notebook import trange, tqdm
# import math
# import torchvision.transforms as T

OFF = 0
ON = 1
HIGH = 2
DEBUG = ON


def create_or_empty(path):
    '''Crea estructura de carpetas vacia para guardar las fotos usadas para tunear el transformer.'''
    if DEBUG >= HIGH:
        print('Precesando carpeta {}'.format(path))
    if os.path.exists(path) or os.path.isdir(path):
        # La carpeta existe. Vaciarla
        if DEBUG >= ON:
            print('Carpeta {} existe. Vaciandola.'.format(path))
        for file in os.scandir(path):
            os.remove(file.path)
    else:
        # La carpeta no existe
        if DEBUG >= ON:
            print('Creando carpeta {}.'.format(path))
        os.mkdir(path)


def main(dataset_origin_path='dataset/photos',
         dataset_output_path='dataset/yelp',
         dataset_json_file='dataset/photos.json',
         max_photos=0):

    '''Crea un repositorio de fotos con la estructura de carpetas requerida para un dataset de Hugging Face.
    
    Para más información:
        create_hf_dataset -h
        
    --dataset_origin_path
        Carpeta donde está el repositório de fotos. Por defecto "dataset/photos".

    --dataset_output_path
        Raiz donde se generará el repositório con la estructura de Hugging Face (split/label/foto).\
            Por defecto "dataset/yelp".
        
    --dataset_json_file
        Fichero JSON con las categorías de las fotos. Por defecto "dataset/photos.json"
        
    --max_photos:
        Número máximo de fotos de cada categoría a procesar. Omitir o cero para procesar todas.\
            número de fotos en train (80%) + test (10%) + evaluate (10%) = max_pphotos'''

    parser = argparse.ArgumentParser("crear_split")
    parser.add_argument(
        "--dataset_origin_path", 
        help="Carpeta donde está el repositório de fotos. Por defecto 'dataset/photos'.", 
        type=str
        )
    parser.add_argument(
        "--dataset_output_path", 
        help="Raiz donde se generará el repositório con la estructura de Hugging Face (split/label/foto).\
            Por defecto 'dataset/yelp'.", 
        type=str
        )
    parser.add_argument(
        "--dataset_json_file", 
        help="Fichero JSON con las categorías de las fotos. Por defecto 'dataset/photos.json'", 
        type=str
        )
    parser.add_argument(
        "--max_photos", 
        help="Número máximo de fotos de cada categoría a procesar. Omitir o cero para procesar todas.\
            número de fotos en train (80%) + test (10%) + evaluate (10%) = max_pphotos", 
        type=int
        )
    args = parser.parse_args()
    
    dataset_origin_path = args.dataset_origin_path if args.dataset_origin_path else 'dataset/photos' #por defecto

    dataset_output_path = args.dataset_output_path if args.dataset_output_path else 'dataset/yelp' #por defecto

    dataset_json_file = args.dataset_json_file if args.dataset_json_file else 'dataset/photos.json' #por defecto

    max_photos = args.max_photos if args.max_photos else 0 #por defecto

    # 1 ##  Crear lista de todas las fotos validas que tienen label (photo_id y label)

    

    # crear listas separadas para train (80% de fotos de cada categoria), test (10%) y validate (10%)

    # crear lista train con max_fotos (usando sampling o over-sampling).
    # Crear listas test y validate con 10% de max_photos

    # crear estructura de carpetas de destino (vaciar carpetas de último nivel si ya existen)

    # copiar archivos a las carpetas de destino




if __name__ == "__main__":
    main()
