import warnings

from Bio import SeqIO


def fasta_extraction(fasta_file, auto_fix=False):
    """Using biopython to check sanity of fasta file"""
    ids = []
    seqs = []
    sanity = False

    # check if file exists and sanity
    try:
        SeqIO.read(fasta_file, "fasta")
    except FileNotFoundError or IOError or AttributeError or IndexError or KeyError or TypeError or ValueError:
        return sanity, ids, seqs

    # if auto_fix
    if auto_fix:
        nucleic_acids = set("ATCGURYSWKMBDHVN")
        for record in SeqIO.parse(fasta_file, "fasta"):
            warnings.warn("You are using auto_fix, which will convert all sequence to RNA alphabet")
            ids.append(record.id)
            seq = str(record.seq).upper().replace("T", "U")
            seq = "".join("N" if n not in nucleic_acids else n for n in seq)
            seqs.append(seq)
        sanity = True
        return sanity, ids, seqs

    for record in SeqIO.parse(fasta_file, "fasta"):
        ids.append(record.id)
        seqs.append(record.seq)
    sanity = True
    return sanity, ids, seqs
