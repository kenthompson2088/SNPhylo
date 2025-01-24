import re
import sys
import os.path

def help(error_no):
    print("Remove SNP data which have many samples which have no SNP information")
    print()
    print("Version: 07222013")
    print()
    print("Usage:")
    print(f"    {os.path.basename(sys.argv[0])} HapMap_file Maximum_%_of_NSS_number")
    print()
    print("Acronyms:")
    print("    NSS: Sample which has no SNP information")
    sys.exit(error_no)

if len(sys.argv) != 3:
    help(1)

hapmap_file = sys.argv[1]
max_nss_percent = float(sys.argv[2])

if not os.path.exists(hapmap_file):
    print(f"HapMap file ({hapmap_file}) was not found!", file=sys.stderr)
    sys.exit(1)

num_wrong_chr_id = 0
with open(hapmap_file, "r") as file:
    for snp_line in file:
        if snp_line[:3] == "rs#":
            max_num_nss = (len(snp_line.strip().split()) - 11) * (max_nss_percent / 100.0)
            print(snp_line, end='')
        else:
            snp_data = snp_line.strip().split()

            try:
                _ = int(snp_data[2])
            except ValueError:
                num_wrong_chr_id += 1
                continue

            genotype_data = snp_data[11:]
            if genotype_data.count('NN') < max_num_nss:
                print(snp_line, end='')

if num_wrong_chr_id > 0:
    plural = "s" if num_wrong_chr_id > 1 else ""
    print(f"\nWarning: There were {num_wrong_chr_id} unreadable chromosome id{plural}. Identifier for a chromosome should be a number.", file=sys.stderr)
