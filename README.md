# Focus of the IPCC Assessment Reports Has Shifted to Lower Temperatures
This is the repository for the paper "Focus of the IPCC Assessment Reports Has Shifted to Lower Temperatures". It contains all code and data needed to recreate the figures of the publication. 

## Raw Data
The analysis in this repository are based on the raw strings of all IPCC reports published until the end of 11.04.2022. Those were extracted using VIsual LAyout (H-VILA) model by Shen et al. (2022). 

## Data Preparation
Running `read_prepare_data.py` will count mentions of the temperatures and reasons for concern and save them in the results folders. It will also create one large string that contains all IPCC report and will take a random sample (with fixed seed) that was used to determine the true positive rate of the temperature mentions. 

## Plotting
Running `figure_1.py` will create the main figure of the paper. 
Running `supplementary_figures.py` will create the supplementary figures that show
- the distributions of the reasons for concern 
- the distribution of the temperatures based on the working groups and the report type
- the true positive rate for the different temperatures
