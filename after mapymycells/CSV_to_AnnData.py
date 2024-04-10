import scanpy as sc
import scipy.sparse
import pandas as pd
import anndata
import os
import sys

#converting the .csv from the MapMyCells into .h5ad
def main():
    csv_file = input(r"C:\Users\Oveido's Lab\Desktop\Shaza\Rebecca Demo UMAP Run\MERFISH_CellsByGenesFormatted_10xWholeMouseBrain(CCN20230722)_HierarchicalMapping_UTC_1712337660599.csv")
    csv_file = csv_file.strip("\"")

    convert_csv_to_h5ad(csv_file, output_file ="MERFISH_CellsByGenesFormatted_10xWholeMouseBrain(CCN20230722)_HierarchicalMapping_UTC_1712337660599.h5ad")
    
    print("\nAnnData object saved successfully.")


def convert_csv_to_h5ad(input_file,output_file=None):
    if not os.path.isfile(input_file):
        print("File not found")

    if sys.version_info[0]<3:
        from StringIO import StringIO
    else:
        from io import StringIO
        
    #create new column per category
    
    
    df = pd.read_csv(StringIO(input_file))
    obs = pd.DataFrame()
    var = pd.DataFrame()
    count_matrix = df.iloc[:,1:].values()
    
    count_matrix = scipy.sparse.csr_matrix(count_matrix)
    adata = anndata.AnnData(
        X= count_matrix,
        obs=obs,
        var= var
    )
    
    adata.write(output_file, compression="gzip")

    if output_file is None:
        output_file = input_file +".h5ad"

    return adata 


