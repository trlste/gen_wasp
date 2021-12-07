# gen_wasp

## Run
First run
```bash
python3 gen_yx.py -n <num_samples> -p <num_SNP> -q <num_genes> --nan_percent <percent_missing>
```
to generate the X files and the Y files.

Then run
```bash
python3 run_wasp_gen.py -x <x> -y <y> run_wasp_gen.py --target_region_size <t> --min_as_count <a> --min_read_count <r> --min_het_count <h> --min_minor_allele_count <m>
```
with the generated X files and the Y files to run CHT. The output will be cht_results.txt in the same folder. Note that the CHT files needs to be in the same folder as this pipeline.
