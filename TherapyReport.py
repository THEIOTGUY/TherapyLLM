import openai
import json
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
e = datetime.datetime.now()
openai.api_key = os.environ['CHATGPT_API']
Therapist = "Suzan"
messages = [ {"role": "system", "content":  
              "You are a intelligent assistant."} ]
import json

def load_json_from_folder(folder_path):
    try:
        # List all files in the folder
        files = os.listdir(folder_path)

        # Filter for JSON files
        json_files = [file for file in files if file.endswith('.json')]

        if not json_files:
            print(f"No JSON files found in {folder_path}")
            return None

        # Assume the first JSON file in the list (you can modify as needed)
        json_file_path = os.path.join(folder_path, json_files[0])

        # Load JSON data from the file
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        print(f"JSON data loaded from {json_file_path}")
        return data

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

# Example usage:
folder_to_load_json = r"text-generation-webui\logs\chat\Suzan"
data = load_json_from_folder(folder_to_load_json)

# Use the loaded data as needed
if data:
    print(data)
data=str(data)
#print(data)
print("info :-  Date:- {day}:{month}:{year},Time:-{hour}:{minute}".format(day=e.day,month=e.month,year=e.year,hour=e.hour,minute=e.minute))
while True: 
    message = "Therapist Name:-{Therapist}, Read this conversation and create a professional therapy report :- ".format(Therapist=Therapist)+ data + "info :- Date:- {day}:{month}:{year},Time:-{hour}:{minute}".format(day=e.day,month=e.month,year=e.year,hour=e.hour,minute=e.minute)
    if message: 
        messages.append( 
            {"role": "user", "content": message}, 
        ) 
        chat = openai.ChatCompletion.create( 
            model="gpt-3.5-turbo", messages=messages
        ) 
    reply = chat.choices[0].message.content 
    #print(f"ChatGPT: {reply}") 
    messages.append({"role": "assistant", "content": reply})
    break
print(reply.encode("utf-8"))
def format_input_text(input_text):
    # Split the input text into lines
    lines = input_text.strip().split('\n\n')

    # Create tuples of headers and content
    headers_and_content = []
    for line in lines:
        # Split on the first occurrence of ":"
        parts = line.split(':', 1)
        header = parts[0].strip() if len(parts) > 0 else ""
        content = parts[1].strip() if len(parts) > 1 else ""
        headers_and_content.append((header, content))

    return headers_and_content

def create_txt_from_text_with_heading(input_text, heading, output_filename='output.txt', encoding='utf-8'):
    with open(output_filename, 'w', encoding=encoding) as txt_file:
        # Write heading to the text file
        txt_file.write(f"{heading}\n\n")

        # Format input text
        headers_and_content = format_input_text(input_text)

        # Write formatted content to the text file
        for header, content in headers_and_content:
            txt_file.write(f"{header}: {content}\n\n")

# Replace this with your actual reply containing the input text
example_text_input = reply

example_heading = ""

# Call the function to create the TXT file with the provided text input and heading
create_txt_from_text_with_heading(example_text_input, example_heading, 'example_report_with_heading.txt')
def text_to_pdf_with_heading(input_filename, output_filename='output.pdf', heading='Therapy Session Report', encoding='utf-8'):
    # Read the content from the text file
    with open(input_filename, 'r', encoding=encoding) as text_file:
        content = text_file.read()

    # Create a PDF document
    pdf_canvas = canvas.Canvas(output_filename, pagesize=letter)

    # Set font and size for the big heading
    pdf_canvas.setFont("Helvetica-Bold", 18)

    # Add big heading to the PDF
    pdf_canvas.drawCentredString(letter[0] / 2, 750, heading)

    # Set font and size for the text
    pdf_canvas.setFont("Helvetica", 12)

    # Calculate available width for the text based on page size and margins
    available_width = letter[0] - 2 * 50  # 50 units margin on each side

    # Set the starting y-coordinate for the content
    y_position = 720  # Adjusted for the heading

    # Split text into lines
    lines = content.split('\n')

    # Add text to the PDF with proper formatting
    for line in lines:
        # Split the line into words
        words = line.split()

        # Initialize the current line
        current_line = ""

        # Iterate through words to control line width
        for word in words:
            if pdf_canvas.stringWidth(current_line + word, "Helvetica", 12) < available_width:
                current_line += word + " "
            else:
                # Draw the text at the specified position
                pdf_canvas.drawString(50, y_position, current_line.strip())
                y_position -= 15  # Adjust as needed for line height
                current_line = word + " "

        # Draw the remaining part of the line
        pdf_canvas.drawString(50, y_position, current_line.strip())
        y_position -= 15  # Adjust as needed for line height

    # Save the PDF document
    pdf_canvas.save()

# Example usage:
input_text_file = 'example_report_with_heading.txt'
output_pdf_file = 'example_report_with_heading.pdf'

# Call the function to convert the text file to PDF with a big heading
text_to_pdf_with_heading(input_text_file, output_pdf_file)
import os

def delete_files_in_folder(folder_path):
    try:
        # List all files in the folder
        files = os.listdir(folder_path)

        # Iterate through each file and delete it
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

        print(f"All files in {folder_path} have been deleted successfully.")

    except Exception as e:
        print(f"Error occurred: {e}")

# Example usage:
folder_to_delete_files = r"text-generation-webui\logs\chat\Assistant"
delete_files_in_folder(folder_to_delete_files)