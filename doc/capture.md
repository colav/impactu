<center><img src="https://raw.githubusercontent.com/colav/colav.github.io/master/img/Logo.png"/></center>

# Scimago Jr
```
for i in $(seq 1999 1 2024); do wget -O "scimagojr_$i.csv" "https://www.scimagojr.com/journalrank.php?year=$i&type=all&out=xls" && mv "scimagojr_$i.csv" "scimagojr $i.csv"; done
```

# Wikidata

Download the data from https://www.wikidata.org/wiki/Wikidata:Database_download/es
in json format. It requite torrent client.

# Minciencias opendata

please read https://github.com/colav/yuku
