# Algorithm Input and Output Data Definition (IODD)


## Input Data

### Input L1 Data

```{table} Input L1 Data
:name: InData
| Parameter  | Description  | Shape |
|------------|--------------|-------|
| L1B TB      | L1B Brightness Temperature at L, C and X-bands <br> ( H and V polarization) | Full swath or swath section <br> (Nscans, Npos) |
| L1B NeΔT | Random radiometric uncertainty of the channels | Full swath or swath section <br> (Nscans, Npos) |
```

### Auxiliary Data

```{table} Auxiliary Data (36 km grid)
:name: AuxData1
| Parameter  | Description  | Shape |
|------------|--------------|-------|
| LST_ECMWF   | ECMWF Land Surface Temperature  (first priority until CIMR LST is tested)  | (964, 406) |
| soil_texture   | Clay fraction (from FAO)     | (964, 406) |
| LCC   | Land Cover type Classification | (964, 406) |
| albedo  | Vegetation single scattering albedo (from SMOS-IC)  | (964, 406) |
| H   | Surface roughness information (from SMOS-IC)  | (964, 406) |
| DEM  | Digital Elevation Model     | (964, 406) |
| hydrology_mask  | CIMR Hydrology Target mask ({doc}`[RD-1] <applicable_ref_docs>`, MRD-854) | (964, 406) |
```

```{table} Auxiliary Data (9 km grid)
:name: AuxData2
| Parameter  | Description  | Shape |
|------------|--------------|-------|
| LST_ECMWF   | ECMWF Land Surface Temperature  (first priority until CIMR LST is tested)   | (3856, 1624) |
| soil_texture   | Clay fraction (from FAO)     | (3856, 1624) |
| LCC   | Land Cover type Classification | (3856, 1624) |
| albedo  | Vegetation single scattering albedo (from SMOS-IC)  | (3856, 1624) |
| H   | Surface roughness information (from SMOS-IC)  | (3856, 1624) |
| DEM  | Digital Elevation Model     | (3856, 1624) |
| hydrology_mask  | CIMR Hydrology Target mask ({doc}`[RD-1] <applicable_ref_docs>`, MRD-854) | (3856, 1624) |
```

### Input L2 Data

The use of CIMR L2 land surface temperature restrievals (instead of ECMWF land surface temperature data) as 
auxiliary data source for soil moisture retrievals will be evaluated. 


### Output Data

```{table} Output Data (36 km grid)
:name: OutData
| Parameter | Description | Units | Shape |
|-----------|-------------|-------|-------|
| time | Time of observation | seconds | (964, 406) |
| EASE row index | Row index in EASE2 grid | - | (964, 406) |
| EASE column index | Column index in EASE2 grid | - | (964, 406) |
| lon | Longitude [0$^{\circ}$, 360$^{\circ}$] | *deg East* | (964, 406) |
| lat | Latitude [90$^{\circ}$S, 90$^{\circ}$N] | *deg North* | (964, 406) |
| SM | Soil Moisture | *m$^{3}$/m$^{3}$* | (964, 406) |
| VOD  | Vegetation Optical Depth | - | (964, 406) |
| TB_L | Gridded L-band TB | *K* | (964, 406) |
| TB_L_RMSE | RMSE between measured and modeled TB | *K* | (964, 406) |
| scene_flags | Flag to indicate difficult inversion situations | *8-bit flag* | (964, 406) |
| status_flag | Product quality flag | *n/a* | (964, 406) |
```


```{table} Output Data (9 km grid)
:name: OutData2
| Parameter | Description | Units | Shape |
|-----------|-------------|-------|-------|
| time | Time of observation | seconds | (3856, 1624) |
| EASE row index | Row index in EASE2 grid | - | (3856, 1624) |
| EASE column index | Column index in EASE2 grid | - | (3856, 1624) |
| lon | Longitude [0$^{\circ}$, 360$^{\circ}$] | *deg East* | (3856, 1624) |
| lat | Latitude [90$^{\circ}$S, 90$^{\circ}$N] | *deg North* | (3856, 1624) |
| SM_E | Soil Moisture (enhanced in spatial resolution) | *m$^{3}$/m$^{3}$* | (3856, 1624) |
| VOD_E  | Vegetation Optical Depth (enhanced in spatial resolution) | - | (3856, 1624) |
| TB_L_E | Gridded enhanced L-band TB  | *K* | (3856, 1624) |
| TB_L_E_RMSE | RMSE between enhanced and modeled TB | *K* | (3856, 1624) |
| scene_flags | Flag to indicate difficult inversion situations | *8-bit flag* | (3856, 1624) |
| status_flag | Product quality flag | *n/a* | (3856, 1624) |
```
