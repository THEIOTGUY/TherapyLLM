from datasets import load_dataset, Dataset

# Load the dataset
dataset = load_dataset("json", data_files=r"C:\Users\Ayush\Downloads\vicunaformatfixedfinal.json")

# Define a function to transform the data
def transform_conversation(entry):
    transformed_entries = []

    print(f"Identity ID: {entry['id']}")
    conversation_pairs = []
    for oneconversation in entry['conversations']:
        if oneconversation['from'] == 'human':
            conversation_pairs.append({'user': oneconversation['value']})
        elif oneconversation['from'] == 'gpt':
            if conversation_pairs:  # Ensure there's a corresponding user utterance
                conversation_pairs[-1]['assistant'] = oneconversation['value']

    for pair in conversation_pairs:
        if 'user' in pair and 'assistant' in pair:
            user_text = pair['user']
            assistant_text = pair['assistant']
            transformed_entry = f"<s>[INST] {user_text}[/INST] {assistant_text}</s>"
            transformed_entries.append(transformed_entry)

    return transformed_entries

# Apply the transformation to the entire dataset
transformed_identities = []
for identity in dataset['train']:
    transformed_identities.extend(transform_conversation(identity))

# Print the number of entries in the transformed dataset
print(f"Number of entries in transformed dataset: {len(transformed_identities)}")

# Convert the transformed data back to a dataset
transformed_dataset = Dataset.from_dict({"train": transformed_identities})

# Push the transformed dataset to the hub
transformed_dataset.push_to_hub("Ayush2312/Therapydataset_formatted_807K", token=True)

# Check if the dataset is not empty before printing the first row
if len(transformed_dataset['train']) > 0:
    print(transformed_dataset['train'][0])
else:
    print("No data in the transformed dataset.")
