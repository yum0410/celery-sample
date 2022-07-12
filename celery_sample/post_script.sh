#!/bin/bash
base_dir='/Users/furutani/Desktop/pan_img'
post_url='http://127.0.0.1:8080/upload'
embed_rul='http://127.0.0.1:8080/embed'

files=(`ls -1 ${base_dir}`)
for file_name in "${files[@]}"; do
    echo "=====CALL ${file_name}====="
    file_id=`curl -L -F "file=@${base_dir}/${file_name}" ${post_url}`
    file_id=`echo ${file_id} | sed -e "s/\"//g"`
    curl ${embed_rul}\/${file_id}
    echo "=====DONE ${file_name}====="
done