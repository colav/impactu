<center><img src="https://raw.githubusercontent.com/colav/colav.github.io/master/img/Logo.png"/></center>

# kahi samples
The first thing is to install https://github.com/colav/Kahi_sample  and https://github.com/colav/Kahi

The samples are:
* `kahi_sample_vip.yml` is the workflow to generate samples for authors

Please run the workflow with 
`kahi_run --workflow kahi_sample_vip.yml`

the output are databases such as:
* minciencias_sample
* openalex_sample
* scholar_sample
* scienti_sample

Then the ETL with kahi can be processed with sample data instead of full datasets at least for those 4 databases.

NOTA: you can mix dbs as CIARP or staff with the sample dbs, it doesn't takes long time executing.