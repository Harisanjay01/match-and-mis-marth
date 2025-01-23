from flask import Flask, request, jsonify, send_file
import pandas as pd
from io import BytesIO

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_files():
    # Get the files from the request
    file1 = request.files['file1']
    file2 = request.files['file2']
    
    # Read Excel files into pandas DataFrames
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    
    # Assume the columns are named 'AWB' and 'Weight'
    df1 = df1[['AWB', 'Weight']]
    df2 = df2[['AWB', 'Weight']]
    
    # Merge the two DataFrames on AWB to find matching entries
    matched = pd.merge(df1, df2, on='AWB', suffixes=('_file1', '_file2'))
    mismatched_file1 = df1[~df1['AWB'].isin(df2['AWB'])]
    mismatched_file2 = df2[~df2['AWB'].isin(df1['AWB'])]
    
    # Convert DataFrames to CSV for download
    matched_csv = matched.to_csv(index=False)
    mismatched_csv1 = mismatched_file1.to_csv(index=False)
    mismatched_csv2 = mismatched_file2.to_csv(index=False)
    
    # Convert to BytesIO objects for sending as downloads
    matched_csv_file = BytesIO(matched_csv.encode())
    mismatched_csv_file1 = BytesIO(mismatched_csv1.encode())
    mismatched_csv_file2 = BytesIO(mismatched_csv2.encode())
    
    matched_csv_file.seek(0)
    mismatched_csv_file1.seek(0)
    mismatched_csv_file2.seek(0)
    
    # Return the files as downloadable links
    return jsonify({
        'matched': 'data:text/csv;base64,' + base64.b64encode(matched_csv_file.read()).decode('utf-8'),
        'mismatched_file1': 'data:text/csv;base64,' + base64.b64encode(mismatched_csv_file1.read()).decode('utf-8'),
        'mismatched_file2': 'data:text/csv;base64,' + base64.b64encode(mismatched_csv_file2.read()).decode('utf-8')
    })

if __name__ == '__main__':
    app.run(debug=True)
