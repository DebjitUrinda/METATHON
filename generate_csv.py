import pandas as pd
import random

# Create a list of example sentences for 'Problem' and 'Factual'
problem_sentences = [
    "My computer is not responding.",
    "I can't access the internet.",
    "The application crashed.",
    "I forgot my password.",
    # Add more 'Problem' sentences here
]

factual_sentences = [
    "The sun rises in the east.",
    "Water boils at 100 degrees Celsius.",
    "The capital of France is Paris.",
    "The Earth orbits the Sun.",
    # Add more 'Factual' sentences here
]

# Create a DataFrame with 100 'Problem' and 100 'Factual' records
data = {
    'Text': random.choices(problem_sentences, k=100) + random.choices(factual_sentences, k=100),
    'Label': (['Problem'] * 100) + (['Factual'] * 100),
}

df = pd.DataFrame(data)

# Save the DataFrame as a CSV file
df.to_csv('problem_factual_dataset.csv', sep='|', index=False)
