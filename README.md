# NEMAParse

Cameron F. Abrams, <cfa22@drexel.edu>

This is set of scripts for parsing completed surveys in the NEMA/xlsx format and generating custom plots.

Suppose you have this folder structure:
```
.
├───2024 survey responses
├───nema_parse
│   ├───data
│   ├───graphics
```

`2024 survey responses` contains all the xlsx files representing the survey responses, and `nema_parse` is this repository, and the working directory.

To parse the responses to build the anonymized data set:
```
python .\parse_em.py -d '..\\2024 survey responses'
```
(this is microsoft/DOS format)

This will generate `data.yml` and `schools.yml` in `nema_parse\data`.  You should probably just delete `schools.yml`.

`analyze_em.py` generates a lot of box-strip plots and scatter plots, and a few 'custom' plots.  The box-strip and scatters are specified in the input file `data\specs.yml`.  The custom plots are hard-coded.  All the plots appear in the `nema_parse\graphics` folder.

`mappy.py` generates a map of the state borders in the Northeast/Mid-Atlantic region and locates each member institution.  This map appears in `graphics\states.png`.