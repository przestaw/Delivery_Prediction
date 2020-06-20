#!/bin/bash

echo '# get project info'
curl -X GET localhost:5000/api/info

sleep 0.2
echo '# load knn model'
curl --header "Content-Type: application/json" \
--request POST  \
--data '{"name": "knn model", "filename": "knn_model.pkl"}' \
http://localhost:5000/api/prediction/models

sleep 0.2
echo '# get loaded models'
curl -X GET localhost:5000/api/prediction/models  

sleep 0.2
echo '# get prediction'
curl --header "Content-Type: application/json" \
--request GET \
--data '{"delivery_company":"360", "city":"Warszawa", "price":10.23, "category":"Gry i konsole", "subcategory":"Gry na konsole"}' \
http://localhost:5000/api/prediction

sleep 0.2
echo '# load tree model'
curl --header "Content-Type: application/json" \
--request POST  \
--data '{"name": "tree model", "filename": "tree_model.pkl"}' \
http://localhost:5000/api/prediction/models
curl -X GET localhost:5000/api/prediction/models  

sleep 0.2
echo '# set up A/B'
curl --header "Content-Type: application/json" \
--request POST  \
--data '{"A": "tree model", "B": "knn model"}' \
http://localhost:5000/api/prediction/AB/models

sleep 0.2
echo '# activate A/B'
curl --header "Content-Type: application/json" \
--request POST \
--data '{"active": true}' \
http://localhost:5000/api/prediction/AB

sleep 0.2
echo '# get prediction'
curl --header "Content-Type: application/json" \
--request GET \
--data '{"delivery_company":"620", "city":"Warszawa", "price":1011.11, "category":"Telefony i akcesoria", "subcategory":"Telefony stacjonarne"}' \
http://localhost:5000/api/prediction

sleep 0.2
echo '# get prediction'
curl --header "Content-Type: application/json" \
--request GET \
--data '{"delivery_company": "516", "city":"Police", "price":351.0, "category":"Komputery", "subcategory":"Drukarki i skanery"}' \
http://localhost:5000/api/prediction

sleep 0.2
echo '# deactivate A/B'
curl --header "Content-Type: application/json" --request POST  \
--data '{"active": false}' \
http://localhost:5000/api/prediction/AB

sleep 0.2
echo '# activate tree model'
curl --header "Content-Type: application/json" --request POST  \
--data '{"name": "tree model"}' \
http://localhost:5000/api/prediction/models/active

sleep 0.2
echo '# check active model'
curl -X GET localhost:5000/api/prediction/models/active

sleep 0.2
echo '# get history'
curl -X GET localhost:5000/api/prediction/history

sleep 0.2
echo '# get summary'
curl -X GET localhost:5000/api/prediction/summary   



