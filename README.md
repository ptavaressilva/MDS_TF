# Preparación TF MDS

Para usar Jupyter Notebook en un contenedor Docker:
1. Cear archivo 'env/.env' con
   
```
TF_MDS_repo1_host=/path/en/mi/ordenador
TF_MDS_repo1_cont=/path/en/el/contenedor
TF_MDS_repo2_host=/otro/path/en/mi/ordenador
TF_MDS_repo2_cont=/otro/path/en/el/contenedor
```

2. Ejecutar script `env/start.sh`
3. Pegar en el nevegador la URL presentada en el terminal (http://127.0.0.1:8888/...)

## Notebooks

[00 EDA](00_EDA.ipynb)

- Análisis exploratório de las fotos y etiquetas

[01 Preparación de datos](01_preparaci'$'\303\263''n_de_los_datos.ipynb)
- Redimensionamiento y recorte de las fotos

[02 Crear dataser con estructura Hugging Face](02_crear_estructura_dataset_HF.ipynb)
- Crea dataset con la estructura requerida por &#129303; Hugging Face
- Genera fotos (augmentatio) para equilibrar dataset

[03 Tunear modelo ViT](03_tuneo_ViT.ipynb)
- Tunear modelo ViT pre-entrenado usando el toy dataset
- Tunear modelo ViT pre-entrenado usando el dataset Yelp completo

[03 Tunear modelo DeiT](04_tuneo_DeiT.ipynb) -WIP
- Tunear modelo DeiT pre-entrenado usando el toy dataset
