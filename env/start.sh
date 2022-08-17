export $(grep -v '^#' ./.env | xargs)

docker run -it -p 8888:8888 \
           -v ${TF_MDS_repo1_host}:${TF_MDS_repo1_cont} \
           -v ${TF_MDS_repo2_host}:${TF_MDS_repo2_cont} \
           --name ds-TF_MDS \
           ptavaressilva/datascience:v3 \
           jupyter notebook --no-browser --allow-root --ip 0.0.0.0

# docker exec -it ds-TF_MDS /bin/bash