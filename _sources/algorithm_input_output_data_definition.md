# Algorithm Input and Output Data Definition (IODD)


## Input Data

### Input L1 Data

```{table} Input L1 Data
:name: InData
| Parameter  | Description  | Shape |
|------------|--------------|-------|
| L1B TB      | L1B Brightness Temperature at L, C and X-bands <br> (H and V polarization) | Full swath or swath section <br> (Nscans, Npos) |
| L1B NeΔT | Random radiometric uncertainty of the channels | Full swath or swath section <br> (Nscans, Npos) |
```

### Auxiliary Data

```{table} Auxiliary Data (36 km grid)
:name: AuxData1
| Parameter  | Description  | Shape* |
|------------|--------------|-------|
| LST_ECMWF   | ECMWF Land Surface Temperature <br> (first priority until CIMR LST is tested)  | (964, 406) |
| soil_texture   | Clay fraction (from FAO)     | (964, 406) |
| LCC   | Land Cover type Classification | (964, 406) |
| albedo  | Vegetation single scattering albedo  | (964, 406) |
| H   | Surface roughness informationn | (964, 406) |
| DEM  | Digital Elevation Model     | (964, 406) |
| hydrology_mask  | CIMR Hydrology Target mask ({doc}`[RD-1] <applicable_ref_docs>`, MRD-854) | (964, 406) |
```

```{table} Auxiliary Data (9 km grid)
:name: AuxData2
| Parameter  | Description  | Shape* |
|------------|--------------|-------|
| LST_ECMWF   | ECMWF Land Surface Temperature <br> (first priority until CIMR LST is tested)   | (3856, 1624) |
| soil_texture   | Clay fraction (from FAO)     | (3856, 1624) |
| LCC   | Land Cover type Classification | (3856, 1624) |
| albedo  | Vegetation single scattering albedo | (3856, 1624) |
| H   | Surface roughness information | (3856, 1624) |
| DEM  | Digital Elevation Model     | (3856, 1624) |
| hydrology_mask  | CIMR Hydrology Target mask ({doc}`[RD-1] <applicable_ref_docs>`, MRD-854) | (3856, 1624) |
```


\* Shapes are equivalent to the global EASE2 grids at 36 km and 9 km resolution, respectively. 
The final grid resolutions will be decided based on further tests on the tradeoff between noise and spatial resolution.

### Input L2 Data

At the current state, no CIMR L2 outputs are used as an input to the CIMR soil moisture retrieval algorithm. The use of CIMR L2 land surface temperature retrievals (instead of ECMWF land surface temperature data) as 
auxiliary data source for soil moisture retrievals will be evaluated. 


### Output Data  

```{table} L2 Processor Output Data (36 km grid)
:name: OutData
| Parameter | Description | Units | Shape* |
|-----------|-------------|-------|-------|
| SM | Soil Moisture | *m$^{3}$/m$^{3}$* | (964, 406) |
| VOD  | Vegetation Optical Depth | - | (964, 406) |
| scene_flags | Flag to indicate difficult inversion situations | *8-bit flag* | (964, 406) |
| status_flag | Retrieval status flag | *n/a* | (964, 406) |
| TBV_L | Gridded L-band TBV | *K* | (964, 406) |
| TBH_L | Gridded L-band TBH | *K* | (964, 406) |
| TB_L_RMSE | RMSE between measured and modeled TB | *K* | (964, 406) |
```


```{table} L2 Processor Output Data (9 km grid)
:name: OutData2
| Parameter | Description | Units | Shape* |
|-----------|-------------|-------|-------|
| SM_E | Soil Moisture (enhanced resolution) | *m$^{3}$/m$^{3}$* | (3856, 1624) |
| VOD_E  | Vegetation Optical Depth (enhanced resolution) | - | (3856, 1624) |
| scene_flags | Flag to indicate difficult inversion situations | *8-bit flag* | (3856, 1624) |
| status_flag | Retrieval status flag | *n/a* | (3856, 1624) |
| TBV_L_E | Gridded L-band TBV (enhanced resolution) | *K* | (3856, 1624) |
| TBH_L_E | Gridded L-band TBH (enhanced resolution) | *K* | (3856, 1624) |
| TB_L_E_RMSE | RMSE between measured and modeled TB (enhanced resolution) | *K* | (3856, 1624) |
```


\* Shapes are equivalent to the global EASE2 grids at 36 km and 9 km resolution, respectively. 
The final grid resolutions will be decided based on further tests on the tradeoff between noise and spatial resolution.
