# gen_wasp

## Run
First run
```bash
python3 gen_yx.py -n <num_samples> -p <num_SNP> -q <num_genes> --nan_percent <percent_missing>
```
to generate the X files and the Y files.

Then run
```bash
python3 run_wasp_gen.py -x <x> -y <y>
```
with the generated X files and the Y files to output the necessary files to run step 5 of CHT (get_target_regions.py)
