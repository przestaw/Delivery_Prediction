# Delivery_Prediction

Project for the Machine Learning Engineering classes at the Faculty of Electronics and Information Technologies, Warsaw University of Technology.

The aim of this project was to invent and implement webservice for delivery time predicion based on historical data.

## Authors

[Przemysław Stawczyk](https://github.com/przestaw)

[Maciej Szulik](https://github.com/shoolic)

## Features

- model training
- models exporting & loading
- serving predictions by *flask* restful api
- A/B experiment 
- prediction summary

## Research

In */notebooks* subfolder there are *IPython* notebooks with data exploration and models comparison steps of our project

## Demonstration

  Demo script utilizing curl *run_curl_demo.sh* executes scenario :
  1. request authors information
  2. load knn model
  3. list models
  4. get prediction
  5. load tree model
  6. configure A/B *(A as tree B as knn)*
  7. activate A/B experiment
  8. get prediction 
  9. get prediction
  10. disable A/B
  11. set tree model as current model
  12. get prediction history
  13. get prediction summary (with responses of all models)
