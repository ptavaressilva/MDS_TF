#!/usr/bin/env python
# coding=utf-8

import pandas as pd
from PIL import Image
import os
import shutil
from torchvision import transforms as T
from torch import manual_seed
import random
import argparse
import pickle

random_state = 42  # La solución de Douglas Adams para todo
# para torchvision
manual_seed(random_state)
random.seed(random_state)


def main(dataset_origin_path='dataset/photos',
         dataset_output_path='dataset/yelp',
         dataset_json_file='dataset/photos.json',
         max_photos=0):
    '''Crea repositorio de fotos con la estructura de carpetas requerida para un dataset de Hugging Face.

    dataset_origin_path
        Carpeta donde está el repositório de fotos.
        Por defecto "dataset/photos".

    dataset_output_path
        Raiz donde se generará el repositório con la estructura de Hugging Face (split/label/foto).
        Por defecto "dataset/yelp".

    dataset_json_file
        Fichero JSON con las categorías de las fotos. Por defecto "dataset/photos.json"

    max_photos:
        Número máximo de fotos de cada categoría a procesar. Omitir o cero para procesar todas.
        Número de fotos en train (80%) + test (10%) + evaluate (10%) = max_pphotos'''

    # Crear lista de fotos validas que tienen label

    if os.path.exists('checkpoints/valid.pkl'):
        print('Listado de fotos disponible en "checkpoints/valid.pkl"')
        df = pickle.load(open('checkpoints/valid.pkl','rb'))
        print('Listado de fotos cargado.')
    else:
        print('No existe listado de fotos en "checkpoints/valid.pkl". Creandolo.')
        df = pd.read_json(open(dataset_json_file, 'rb'), lines=True)
        df = df.drop(columns=['business_id', 'caption'])
        contador = 0
        discarded = 0
        for img in df.photo_id.tolist():
            if (contador % 30 == 0) and (contador > 0):
                print('Procesadas {:7,} mil fotos de las cuales {} están corruptas'.format(
                    contador,
                    discarded
                ),
                    end='\r')
            contador += 1
            try:
                img = Image.open(dataset_origin_path + '/' + img+'.jpg')
                img.verify()
            except:
                # file is corrupt
                df = df.drop(df.loc[df.photo_id == img].index)
                discarded += 1
        print('Procesadas {:7,} mil fotos de las cuales {} están corruptas'.format(
            contador, discarded))
        print('Guardando listado de fotos validas en "checkpoints/valid.pkl".')
        pickle.dump(df, open('checkpoints/valid.pkl', 'wb'))

    # crear listas separadas para train (80% de max_photos), test (10%)
    # y validation (10%) en cada categoria

    categorias = df.label.value_counts().index

    dataset = {'train': {},
               'test': {},
               'validation': {}}

    for categoria in categorias:
        print('Creando dataframes con slices para "{}" usando fotos originales'.format(categoria))
        # 80% de max_photos
        slice_80 = int(len(df.loc[df.label == categoria]) * 0.8)
        # 10% de max_photos
        slice_10 = int(len(df.loc[df.label == categoria]) * 0.1)
        dataset['train'].update(
            {categoria: df.loc[df.label == categoria][0:slice_80]})
        dataset['test'].update(
            {categoria: df.loc[df.label == categoria][slice_80:slice_80+slice_10]})
        dataset['validation'].update(
            {categoria: df.loc[df.label == categoria][slice_80+slice_10:]})

    subset_max_photos = {  # número máximo de fotos de cada categorñia en el split
        'train': int(max_photos * 0.8),
        'test': int(max_photos * 0.1)
    }
    subset_max_photos.update({
        # las que quedan para sumar max_photos
        'validation': max_photos - subset_max_photos['train'] - subset_max_photos['test']
    })

    # limitar los subsets a max_photos
    for subset in ['train', 'test', 'validation']:
        for categoria in categorias:
            # si hay demasiadas fotos, hacer resample
            if len(dataset[subset][categoria]) > subset_max_photos[subset]:
                print('Sampling de fotos de "{}/{}".'.format(subset, categoria))
                dataset[subset][categoria] = dataset[subset][categoria].sample(n=subset_max_photos[subset],
                                                                               random_state=random_state,
                                                                               replace=False,  # max 1x cada foto
                                                                               ignore_index=True)

    # crear estructura de carpetas (limpiar si ya existia)
    if os.path.isdir(dataset_output_path):
        shutil.rmtree(dataset_output_path, ignore_errors=False,
                      onerror=None)  # remove tree
        print('Carpeta {} eliminada'.format(dataset_output_path))

    os.mkdir(dataset_output_path)
    print('Carpeta {} creada'.format(dataset_output_path))

    for subset in ['train', 'test', 'validation']:
        os.mkdir(dataset_output_path + '/' + subset)
        print('Carpeta {} creada'.format(dataset_output_path + '/' + subset))
        for categoria in categorias:
            os.mkdir(dataset_output_path + '/' + subset + '/' + categoria)
            print('Carpeta {} creada'.format(
                dataset_output_path + '/' + subset + '/' + categoria))

    subset_max_photos = {
        'train': int(max_photos * 0.8),
        'test': int(max_photos * 0.1)
    }

    subset_max_photos.update({
        # las que quedan
        'validation': max_photos - subset_max_photos['train'] - subset_max_photos['test']
    })

    pipeline = T.Compose([
        T.RandomRotation(degrees=(30, 70)),
        T.RandomResizedCrop((224, 224)),
        T.ColorJitter(brightness=.2, hue=.1)
    ])

    # copiar fotos seleccionadas para nuevo repo
    for subset in ['train', 'test', 'validation']:
        for categoria in categorias:

            # copiar archivos a las carpetas de destino
            contador = 0
            for img in dataset[subset][categoria].photo_id:
                shutil.copyfile(dataset_origin_path + '/' + img + '.jpg',
                                dataset_output_path + '/' + subset + '/' + categoria + '/' + img + '.jpg')
                if (contador % 30 == 0) and (contador > 0):
                    print('{} - copiadas {:7,} fotos'.format(dataset_output_path + '/' + subset + '/' + categoria,
                                                             contador),
                          end='\r')
                contador += 1
            print('{} - copiadas {:7,} fotos'.format(dataset_output_path + '/' + subset + '/' + categoria,
                                                     contador))

            # generar imagenes si necesario
            if (len(dataset[subset][categoria]) < subset_max_photos[subset]):  # faltan imagenes

                # determinar cuantas imagenes tendremos que generar
                n_missing = subset_max_photos[subset] - len(dataset[subset][categoria])

                print('Faltan {} imagenes en {}\\{}'.format(n_missing, subset, categoria))

                # seleccionar imagenes que vamos usar como base
                if n_missing > len(dataset[subset][categoria]):
                    # necesitamos generar más imagenes que las que tenemos en origen
                    df_base_images = dataset[subset][categoria].sample(n=n_missing,
                                                                    random_state=random_state,
                                                                    replace=True,  # habrá fotos duplicadas
                                                                    ignore_index=True)
                else:
                    df_base_images = dataset[subset][categoria].sample(n=n_missing,
                                                                    random_state=random_state,
                                                                    replace=False,  # todas fotos distintas
                                                                    ignore_index=True)

                # abrir original > transformar > guardar imagen transformada > añadir nueva foto al subset
                contador = 0
                for img_name in df_base_images.photo_id:
                    original_image_path = dataset_origin_path + '/' + img_name + '.jpg'
                    new_image_path = dataset_output_path + '/' + subset + \
                        '/' + categoria + '/' + img_name + '_tr{}.jpg'.format(contador)
                    with Image.open(original_image_path) as img:
                        augmented_image = pipeline(img=img)
                        augmented_image.save(new_image_path)

                    new_img = pd.DataFrame(data={'photo_id': img_name+'_tr{}.jpg'.format(contador),
                                                'label': df.loc[df.photo_id == img_name].label})
                    dataset[subset][categoria] = pd.concat(
                        [dataset[subset][categoria], new_img])
                    if (contador % 30 == 0) and (contador > 0):
                        print('{} - generadas {:7,} fotos'.format(dataset_output_path + '/' + subset + '/' + categoria,
                                                                contador),
                            end='\r')
                    contador += 1

                print('{} - generadas {:7,} fotos'.format(dataset_output_path + '/' + subset + '/' + categoria,
                                                      contador))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("create_hf_dataset")
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
            número de fotos en train (80%%) + test (10%%) + evaluate (10%%) = max_photos",
        type=int
    )

    args = parser.parse_args()

    dataset_origin_path = args.dataset_origin_path if args.dataset_origin_path else 'dataset/photos'  # por defecto

    dataset_output_path = args.dataset_output_path if args.dataset_output_path else 'dataset/yelp'  # por defecto

    dataset_json_file = args.dataset_json_file if args.dataset_json_file else 'dataset/photos.json'  # por defecto

    max_photos = args.max_photos if args.max_photos else 0  # por defecto

    print('Procesando:\n  dataset_origin_path={}\n  dataset_output_path={}\n  dataset_json_file={}\n  max_photos={}'.format(dataset_origin_path, dataset_output_path, dataset_json_file, max_photos))

    main(dataset_origin_path, dataset_output_path, dataset_json_file, max_photos)
