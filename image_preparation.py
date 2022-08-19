from email.mime import image
import pickle
import pandas as pd
import os
from PIL import Image
from tqdm.notebook import trange, tqdm
import math
import torchvision.transforms as T

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


def main(dataset_photos_path = 'dataset/photos',
    dataset_output_path = 'dataset/recortadas',
    photo_size = 224,
    df_pickle_file='checkpoints/df5.pkl',
    max_photos=100):
    '''Crea una replica de las fotos en formato png, redimensionadas y recortadas 224x224, 
    organizadas por etiqueta.
    
    dataset_photos_path: carpeta en la que se encuentran las fotos originales.
    
    dataset_output_path: carpeta donde se volcarán las fotos recortadas.
    
    photo_size: tamaño de las fotos recortadas.
    
    df_pickle_file: nombre del fichero Pickle con el listado de fotos validas del dataset(creado al ejecutar 00_EDA.ipynb)
    
    max_photos: número máximo de fotos de cada categoría a procesar. 0 para procesar todas.'''

    df = pickle.load(open(df_pickle_file,'rb'))

    if max_photos > 0: # procesar solo un sub-conjunto de las fotos
        df_subset = pd.DataFrame([], columns=['photo_id',
                                        'label',
                                        'x_dim', 
                                        'y_dim', 
                                        'z_channels', 
                                        'pixels', 
                                        'drink',
                                        'food',
                                        'inside',
                                        'menu',
                                        'outside'])
        total_photos = df.label.value_counts()
        for label in total_photos.index:
            if total_photos[label] > max_photos: # Hay muchas fotos. Preservar un subconjunto.
                df_subset = pd.concat([df_subset,
                                    df.loc[df.label == label].sample(n=max_photos)])
            else: # Hay pocas fotos. Preservar todas.
                df_subset = pd.concat([df_subset,
                                    df.loc[df.label == label]])
        df = df_subset
        del(df_subset)

    if not (os.path.exists(dataset_output_path) or os.path.isdir(dataset_output_path)):
        # La carpeta dataset_output_path no existe. Crearla.
        os.mkdir(dataset_output_path)

    categories = df.label.value_counts().index
    for category in categories:
        create_or_empty('{}/{}'.format(dataset_output_path, category))

    # redimensionar, recortar y guardar fotos

    for img in tqdm(range(len(df)), desc='Photos cropped', miniters=len(df)//100):
        im = Image.open('{}/{}.jpg'.format(dataset_photos_path, df.iloc[img].photo_id))
        
        # redimensionar
        if (df.iloc[img].y_dim < df.iloc[img].x_dim): # imagen estrecha
            width = int(photo_size)
            height = math.floor(photo_size * df.iloc[img].x_dim/df.iloc[img].y_dim)
        else: # imagen ancha
            width = math.floor(photo_size * df.iloc[img].y_dim/df.iloc[img].x_dim)
            height = int(photo_size)
                    
        resized = T.Resize((height, width))(im)
        cropped = T.CenterCrop(size=int(photo_size))(resized)
                
        cropped.save('{}/{}/{}.png'.format(
            dataset_output_path, 
            df.iloc[img].label, 
            df.iloc[img].photo_id))
   
if __name__ == "__main__":
    main()