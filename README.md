# Preparación TF MDS
Descargar el [dataset de fotos de Yelp](https://www.yelp.com/dataset) en la carpeta /dataset

En Linux usar comando `tar -xf yelp_photos.tar` para descomprimir fichero. Crea carpeta `/dataset/photos` con las fotos y fichero `/dataset/photos.json` con las etiquetas.

## EDA
Análisis exploratório de las fotos y etiquetas
- [00 EDA](00_EDA.ipynb)

## Preparación de los datos y Modelación

### CNN con toy dataset

1. [Preparación de los datos](01_Preparación_flat_toy_dataset.ipynb)
2. [Entrenamiento](04_CNN_toy.ipynb)

### CNN con dataset 5k

1. Preparación de los datos
2. Entrenamiento

### ViT (&#129303; Hugging Face)

1. [Preparación de los datos](01_preparación_de_los_datos.ipynb)
2. [Entrenamiento (toy y completo)](03_tuneo_ViT.ipynb)

### DeiT (&#129303; Hugging Face) - **WIP**

1. [Preparación de los datos (toy y 5k)](02_crear_estructura_dataset_HF.ipynb)
2. [Entrenamiento](04_tuneo_DeiT.ipynb) - &#9888; ver error en [Stack Overflow](https://stackoverflow.com/questions/73505595/forward-got-an-unexpected-keyword-argument-labels-while-training-huggin-fa)

WIP = work in progress (trabajo en curso)

## MLflow Tracking

1. [Instrucciones](MAN_MLflow.ipynb)
2. [Ejemplo con CNN / Keras](04_CNN_toy_MLflow.ipynb)

## Entorno
Para usar Jupyter Notebook en un contenedor Docker (requiere Docker Desktop instalado en el host):
1. Cear archivo 'env/.env' con
   
```
TF_MDS_repo1_host=/path/en/mi/ordenador
TF_MDS_repo1_cont=/path/en/el/contenedor
TF_MDS_repo2_host=/otro/path/en/mi/ordenador
TF_MDS_repo2_cont=/otro/path/en/el/contenedor
```
**WINDOWS**: si el host es Windows los path tienen el formato //C/Users/USERNAME/...

2. Ejecutar script `env/start.sh`
3. Pegar en el nevegador la URL presentada en el terminal (http://127.0.0.1:8888/...)

Configurar Git:
1. Abrir terminal del contenedor con `docker exec -it ds-TF_MDS /bin/bash`
2. Configurar usar con `git config --global user.email "you@example.com"`y `git config --global user.name "Your Name"`

Hacer login en GitHub:
1. usar comando `gh auth login`
2. "Authenticate Git with your GitHub credentials?" = "Yes"
3. Login with a web browser
4. Abrir un navegador e ir a "https://github.com/login/device"
5. Pegar en el navegador el código (XXXX-XXXX) que aparece en el terminal.