
import pandas as pd

def find_ligand_receptors(single_cell_data):
    ''' Finds the ligands and receptors that are in the user's single cell data

    Args:
        single_cell_data (_type_): _description_

    Returns:
        _type_: _description_
    '''
    gene_input_file = pd.read_csv("/Users/derekebowman/Coding Projects/stPercolate/data/cellphonedb-data-5.0.0/data/gene_input.csv")
    protein_input_file = pd.read_csv("/Users/derekebowman/Coding Projects/stPercolate/data/cellphonedb-data-5.0.0/data/protein_input.csv")
    interaction_input = pd.read_csv("/Users/derekebowman/Coding Projects/stPercolate/data/cellphonedb-data-5.0.0/data/interaction_input.csv")
    relevant_genes = list(single_cell_data.var.index)
  
    # relevant_genes = [gene.capitalize() for gene in relevant_genes]

    matching_genes = gene_input_file[
        gene_input_file["gene_name"].isin(relevant_genes)
    ]
    
    genes_protein_combined = matching_genes.merge(protein_input_file, on='uniprot', how='inner')
    
    relevant_receptors = genes_protein_combined[
        genes_protein_combined['receptor'] == True]
    
    relevant_ligands = genes_protein_combined[
        genes_protein_combined['receptor'] == False]
    
    receptor_interactions = interaction_input[interaction_input['partner_b'].isin(relevant_receptors['uniprot'])]
    
    receptor_interactions[receptor_interactions['partner_a'].isin(genes_protein_combined['uniprot'])]
    
    #receptor_interactions['partner_a'].str.capitalize()
    
    return matching_genes, relevant_receptors, relevant_ligands, receptor_interactions  # I need to make a function that associates the genes with the protid.



'''
def 

Genes in the single cell data base should be used to find only relevant genes and receptors.

The relevant receptors should be marked as receptors.

For every receptor, find the possible partners a in the database

This partners should be limited to those that are actually present in the single cell databse to begin with.

''' 
    
