#!/bin/bash

echo 'localhost:5000/name'

curl -X GET localhost:5000/name

echo '# Send request : {"delivery_company":"360", "city":"Warszawa", "price":10.23, "category":"Gry i konsole", "subcategory":"Gry na konsole"}'

curl --header "Content-Type: application/json" \
  --request GET \
  --data '{"delivery_company":"360", "city":"Warszawa", "price":10.23, "category":"Gry i konsole", "subcategory":"Gry na konsole"}' \
  http://localhost:5000/api

echo '# Send request : {"delivery_company":"620", "city":"Konin", "price":1000.00, "category":"Gry i konsole", "subcategory":"Gry na konsole"}'

curl --header "Content-Type: application/json" \
  --request GET \
  --data '{"delivery_company":"620", "city":"Konin", "price":1000.00, "category":"Gry i konsole", "subcategory":"Gry na konsole"}' \
  http://localhost:5000/api

echo '# localhost:5000/api/history'

curl -X GET localhost:5000/api/history

echo '# localhost:5000/api/summary'

curl -X GET localhost:5000/api/summary