import sqlite3

def find_gene_sets_with_minimum_overlap(genes, min_overlap=1, db_path=None):
    """ Find gene sets that contain at least N genes from the input list.
    
    Args:
        genes (list): List of gene symbols to search for
        min_overlap (int): Minimum number of genes that must occur in a gene set for that gene set to be included.
    
    Returns:
        list: List of tuples, where each tuple contains the gene set name, the number of overlapping genes, and the overlapping?? # provided by copilot. double check this.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create placeholders for the IN clause
    placeholders = ','.join(['?' for _ in genes])
    
    query = f"""
    SELECT 
        gset.standard_name,
        COUNT(DISTINCT gsym.symbol) as overlap_count,
        GROUP_CONCAT(DISTINCT gsym.symbol) as matching_genes
    FROM gene_set gset
        INNER JOIN gene_set_gene_symbol gsgs ON gset.id = gsgs.gene_set_id
        INNER JOIN gene_symbol gsym ON gsym.id = gsgs.gene_symbol_id
    WHERE symbol in ({placeholders})
    GROUP BY gset.standard_name
    HAVING overlap_count >= ?
    ORDER BY overlap_count DESC;
    """
    
    try:
        # Execute with genes list plus the min_overlap parameter
        cursor.execute(query, genes + [min_overlap])
        results = cursor.fetchall()
        
        print(f"\nFound {len(results)} gene sets with {min_overlap} or more overlapping genes:")
        for name, count, genes in results:
            print(f"\nGene set: {name}")
            print(f"Number of overlapping genes: {count}")
            print(f"Matching genes: {genes}")
            
        return results
        
    finally:
        conn.close()
