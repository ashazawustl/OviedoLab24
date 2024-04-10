# Cell by Gene CSV data by MERFISH to AnnData object for MapMyCells (Allen Institute)

import pandas as pd
import anndata
import scipy.sparse
import numpy as np

import os
import sys
import json


# Cell with less than this threshold of transcripts will be filtered out
TRANSCRIPTS_THRESHOLD = 100



def main():
    # Ask user input for csv file path
    csv_file_path = input(r"C:\Users\Oveido's Lab\Desktop\Shaza\cell_by_gene.csv")

    # The path input may contain quotes, remove them
    csv_file_path = csv_file_path.strip("\"")

    if not os.path.isfile(csv_file_path):
        print("File not found")
        return

    
    # Read the csv file as text for manual parsing
    with open(csv_file_path) as f:
        lines = f.readlines()
    
    print(f"Number of cells detected with MERFISH (in CSV): {len(lines)-1}\n\nProcessing data...") # -1 because the first row is the header

    # split by newline
    lines = [line.strip() for line in lines]

    # Load the json data
    with open("geneName_to_ID.json") as f:
        geneName_to_ID = json.load(f)

    # Turn the keys to lowercases for looser matching just in case
    geneName_to_ID = {key.lower(): value for key, value in geneName_to_ID.items()}


    # Match the gene names to the json data id to replace the first row of the csv

    # Get the list of gene names from the first row of the csv
    gene_names = lines[0].split(",")[1:]
    # To lower case
    gene_names = [gene_name.lower() for gene_name in gene_names]

    # gene_ids to matched the gene_names in order
    gene_ids = []
    for gene_name in gene_names:
        gene_id = geneName_to_ID.get(gene_name, {"id": gene_name})["id"]
        gene_ids.append(gene_id)

        # Note: instead of .get() and default to gene_name, maybe it's better to also print out the gene_name that is not found in the json data?



    # print(len(gene_names), len(gene_ids)) # The two number here should be the same


    # Reconstruction of the csv file by replacing the first row with the gene ids and join them back to a string
    lines[0] = ",".join(["cell_name"] + gene_ids)
    new_csv = "\n".join(lines)

    # Write the new csv file as a variable with StringIO for pandas to read

    if sys.version_info[0] < 3: 
        from StringIO import StringIO
    else:
        from io import StringIO

    df = pd.read_csv(StringIO(new_csv))

    
    obs = pd.DataFrame([{'sample_id': s} for s in df['cell_name']]).set_index('sample_id')
    
    # var is the header with the list of gene names
    var = pd.DataFrame(index=gene_ids)

    # The count matrix is the rest of the csv file
    count_matrix = df.iloc[:, 1:].values

    # Create an AnnData object, the first column is the cell names, and the rest are the gene count
    count_matrix = scipy.sparse.csr_matrix(count_matrix)
    
    countAD = anndata.AnnData(
        X=count_matrix,
        obs=obs,
        var=var)
    # Don't get why AnnData() raises "ImplicitModificationWarning: Transforming to str index."
    


    print(f"\nNumber of cells in raw AnnData: {len(countAD)}") # this should be the same as the number of cells in the csv file

    
    # Filter out cells that have less than TRANSCRIPTS_THRESHOLD transcripts (sum of all genes)
    countAD_filtered = countAD[countAD.X.sum(axis=1) >= TRANSCRIPTS_THRESHOLD, :]
    print(f"Number of cells after filter (>= {TRANSCRIPTS_THRESHOLD} transcripts): {len(countAD_filtered)} ({100 * len(countAD_filtered)/len(countAD)}%)")


    # Save the AnnData object with only the cells that have more than TRANSCRIPTS_THRESHOLD transcripts
    countAD_filtered.write("MERFISH_CellsByGenesFormatted.h5ad", compression="gzip") # also use compression to make file size smaller for MapMyCells


    print("\nAnnData object saved successfully.")

if __name__ == "__main__":
    main()
    

