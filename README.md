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

[01 Preparación de datos](01_preparación_de_los_datos.ipynb)
- Redimensionamiento y recorte de las fotos

