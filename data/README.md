# Data directory

Place NetLogo CSV outputs here when running analyses locally.

Typical migration-screen format:

```text
migration,tick,cell_count
0.0,1,1007
0.0,2,1012
...
```

Typical FBS-screen format:

```text
FBS,tick,cell_count
1.0,1,1002
1.0,2,1004
...
```

Generated CSV outputs are excluded by `.gitignore` by default. If a manuscript requires public raw simulation outputs, remove the relevant ignore rule or deposit the data in a dedicated archival repository and link it from the main README.
