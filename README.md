# Beer Recommender: Finding Your Perfect Brew

Welcome to the Beer Recommender project! My goal is to create a powerful model that recommends the ideal beer for you based on your preferences. I strongly believe that there's a beer out there for everyone, and with my model, I aim to help you discover the ones you'll love.

## How it Works
The input to the model is a phrase or description of the beer you desire. For example, you might say, "I want a beer that goes well with fries and has a hint of vanilla." The model will then generate a list of beers along with their descriptions, providing you with a curated selection that matches your preferences.

## Project Workflow
This project is divided into several key steps:

### Data Scraping:
I collect a substantial amount of beer data, including descriptions, general information such as alcohol content, ratings, beer types, and even some user reviews. This comprehensive dataset serves as the foundation for the model.

### Data Cleaning and Preprocessing:
To prepare the data for model training, I carefully clean and preprocess it, ensuring it is in a suitable format for feeding into the machine learning model.

### Model Development
The primary objective is to construct a model that utilizes all available information about each beer. My current approach involves leveraging a pre-trained SBERT model to obtain sentence embeddings. By utilizing cosine similarity, we can identify the closest sentences (reviews and or description) to your desired input.

Please note that this project is still a work in progress, and im an continuously refining and enhancing the model.

### [beer dashboard](https://lookerstudio.google.com/s/rUDsWY38Mhw)

## Future Steps
Once I have achieved satisfactory results, I plan to deploy the model on a server, making it accessible to anyone seeking personalized beer recommendations. This deployment will allow users to easily obtain beer suggestions tailored to their unique tastes and preferences.

 are excited about the potential of this project and look forward to helping you discover the perfect beer for any occasion. Cheers!

Please feel free to explore the repository, and if you have any questions or suggestions, don't hesitate to reach out.

