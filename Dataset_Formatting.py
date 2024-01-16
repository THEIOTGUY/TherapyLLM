from datasets import load_dataset, Dataset

# Load the dataset
dataset = load_dataset("json", data_files=r"C:\Users\vaida\Downloads\TherapyDataset.json")
# Define a function to transform the data
def transform_conversation(entry):
    reformatted_segments = []

    user_text = None
    assistant_text = None

    print(f"Identity ID: {entry['id']}")
    for oneconversation in entry['conversations']:
        #print(oneconversation)
        if oneconversation['from'] == 'input':
            user_text = f"{oneconversation['value']}"
            reformatted_segments.append(f'[INST] {user_text}')
        elif oneconversation['from'] == 'response':
            assistant_text = f"{oneconversation['value']}"
            reformatted_segments.append(f'[/INST] {assistant_text}')
    return '<s>'+''.join(reformatted_segments)+'</s>'

# Apply the transformation to the entire dataset
transformed_identities = [transform_conversation(identity) for identity in dataset['train']]

# Convert the transformed data back to a dataset
transformed_dataset = Dataset.from_dict({"train": transformed_identities})

# Push the transformed dataset to the hub
transformed_dataset.push_to_hub("Ayush2312/Therapydataset_formatted", token=True)
