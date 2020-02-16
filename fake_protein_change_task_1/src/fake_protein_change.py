from argparse import ArgumentParser,RawDescriptionHelpFormatter
import sys
#import numpy as np
import pandas as pd
from pandas import DataFrame

def parseOptions():
    epilog = """adds or removes artificial Protein_Change field in maf"""
    desc = "modify maf ."
    parser = ArgumentParser(description=desc, formatter_class=RawDescriptionHelpFormatter, epilog=epilog)

    parser.add_argument("-m","--input_maf", type=str, help="Input maf")
    parser.add_argument("-p","--protein_change", type=str, help="fake Protein Change string",default="p.A1A")
    parser.add_argument("-i","--id", type=str, help="id stub prepended to output files.  <id>.<stub>.maf")
    parser.add_argument("-s","--stub", type=str, help=" stub postpended after id to output maf.  <id>.<stub>.maf",default="fake_protein_change")
    parser.add_argument("-r", "--remove_fake_protein_change", action='store_true', help="remove fake Protein Change ")
    parser.add_argument("-x", "--X_chromosome_maf", type=str, help="restore missing X chromosome events ",default="")

    args = parser.parse_args()
    return args

def main():
    args = parseOptions()
    print(args)

    input_maf = args.input_maf
    protein_change = args.protein_change
    id1 = args.id
    stub = args.stub
    remove = args.remove_fake_protein_change
    X_maf = args.X_chromosome_maf

    maf0 = pd.read_csv(input_maf, sep="\t", index_col=None,low_memory=False)
    maf0.head(2)

    maf0 = maf0.drop_duplicates()
    print(maf0['Protein_Change'][0])

    k = maf0.index[maf0['Chromosome'] == 'X'].tolist()
    if (len(X_maf)>0)&(len(k)<1):
        mafX = pd.read_csv(X_maf, sep="\t", index_col=None, low_memory=False)
        mafX.head(2)
        k=mafX.index[mafX['Chromosome'] == 'X'].tolist()
        mafX=mafX.loc[k]
        maf0=maf0.append(mafX,sort=False)
        maf0=maf0.drop_duplicates()


    k1=maf0.loc[pd.notnull(maf0['Protein_Change'])].index.tolist()

    print('#####')
    print(k1)
    print('#####')

    has=(len(k1)>0)

    print(has,remove)

    if remove and has:
      #k=maf0.loc(maf0['Protein_Change'].str.match(protein_change)).index.tolist()
      k=maf0.loc[maf0['Protein_Change'] == protein_change].index.tolist()
      if len(k)>0:
          print(k[0])
          maf0['Protein_Change'][k]=''

    elif not has:
      print('fake protein change: '+protein_change)
      k2=maf0.loc[pd.isnull(maf0['Protein_Change'])].index.tolist()
      maf0['Protein_Change'][k2]=protein_change

    print(id1+"."+stub+".maf")
    maf0.to_csv(id1+"."+stub+".maf", sep="\t", index=None,float_format='%.5f')

    mafSNP=maf0.loc[maf0['Variant_Type'].isin(['SNP','DNP','MNP','ONP'])]
    mafINDEL=maf0.loc[maf0['Variant_Type'].isin(['INS','DEL'])]
    print(id1+"."+stub+".SNP.maf")
    mafSNP.to_csv(id1+"."+stub+".SNP.maf", sep="\t", index=None,float_format='%.5f')
    print(id1+"."+stub+".INDEL.maf")
    mafINDEL.to_csv(id1+"."+stub+".INDEL.maf", sep="\t", index=None,float_format='%.5f')

    return 0

if __name__ == "__main__":
    sys.exit(main())
