import re
import sys
import os.path


def help(error_no):
    print("Remove VCF data which have many low depth of coverage samples")
    print()
    print("Version: 01072016")
    print()
    print(f"Usage: {os.path.basename(sys.argv[0])} VCF_file Minimum_depth_of_coverage Maximum_%_of_LCS_number")
    print()
    print("Acronyms:")
    print("    LCS: Low Coverage Sample")
    sys.exit(error_no)


if len(sys.argv) != 4:
    help(1)

vcf_filepath = sys.argv[1]
min_depth = int(sys.argv[2])
max_lcs_percent = float(sys.argv[3])

if not os.path.exists(vcf_filepath):
    print(f"VCF file ({vcf_filepath}) was not found!", file=sys.stderr)
    sys.exit(1)

num_wrong_chr_id = 0
num_no_dp_data = 0
num_pass_wo_dp_test = 0
num_missing_data = 0
max_num_low_depth_sample = -1

with open(vcf_filepath, "r") as vcf_file:
    for vcf_line in vcf_file:
        if vcf_line[0] == "#":
            print(vcf_line, end='')
            if vcf_line.startswith("#CHROM"):
                max_num_low_depth_sample = (len(vcf_line.strip().split()) - 9) * (max_lcs_percent / 100.0)
        else:
            vcf_data = vcf_line.strip().split()

            if not vcf_data:
                continue

            try:
                _ = int(vcf_data[0])
            except ValueError:
                num_wrong_chr_id += 1
                continue

            format_col = vcf_data[8].split(':')
            format_col_len = len(format_col)

            try:
                dp_col_no = format_col.index('DP')
            except ValueError:
                dp_col_no = -1
                num_no_dp_data += 1

            try:
                gt_col_no = format_col.index('GT')
            except ValueError:
                print(f"\nWarning: CHROM: {vcf_data[0]}, POS: {vcf_data[1]} did not have genotype data.", file=sys.stderr)
                continue

            num_low_depth_sample = 0
            for genotype in vcf_data[9:]:
                # In order to increase processing speed, several 'if' and 'continue' statements were used in this loop.
                genotype_col = genotype.split(':')

                # To check both "./." for a diploid genotype and "." for haploid genotype
                if genotype[0] == "." or genotype_col[gt_col_no][0] == ".":
                    num_low_depth_sample += 1  # Missed genotype data is counted as a low depth data
                else:
                    if dp_col_no > 0:
                        try:
                            if int(genotype_col[dp_col_no]) < min_depth:
                                num_low_depth_sample += 1
                        except ValueError:
                            num_pass_wo_dp_test += 1  # If there is no depth value
                    else:
                        num_pass_wo_dp_test += 1

            if max_num_low_depth_sample < 0:
                print("\nError: There is no header line in the VCF file.", file=sys.stderr)
                sys.exit(1)

            if num_low_depth_sample < max_num_low_depth_sample:
                print(vcf_line, end='')


determine_was_were = lambda x: "were" if x > 1 else "was"

if num_wrong_chr_id > 0:
    print(f"\nWarning: There {determine_was_were(num_wrong_chr_id)} {num_wrong_chr_id} unreadable chromosome id{'s' if num_wrong_chr_id > 1 else ''}. Identifier for a chromosome should be a number.", file=sys.stderr)

if num_no_dp_data > 0:
    print(f"\nWarning: There {determine_was_were(num_no_dp_data)} {num_no_dp_data} SNP position{'s' if num_no_dp_data > 1 else ''} which did not have DP information.", file=sys.stderr)

if num_pass_wo_dp_test > 0:
    print(f"\nWarning: {num_pass_wo_dp_test} SNP{'s' if num_pass_wo_dp_test > 1 else ''} {determine_was_were(num_pass_wo_dp_test)} passed without the read depth assessment because of the absence of the DP column.", file=sys.stderr)
