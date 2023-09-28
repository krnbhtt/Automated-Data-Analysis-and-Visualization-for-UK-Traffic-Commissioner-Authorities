import pandas as pd

def create_chunked_csv(input_file, output_file, chunk_size=500):
    csv_reader = pd.read_csv(input_file, chunksize=chunk_size)
    chunked_data = []

    # Iterate through the chunks and select the first chunk_size rows
    for i, chunk in enumerate(csv_reader):
        chunked_data.append(chunk[:chunk_size])
        if i == 0:
            break

    result_df = pd.concat(chunked_data)

    result_df.to_csv(output_file, index=False)

file_path = 'Data\concatenated_data.csv'
chunk_file_path = 'Data/chunk.csv'

create_chunked_csv(file_path, chunk_file_path)
print(f"Chunk CSV file is saved to {chunk_file_path}")
