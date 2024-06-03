# Algorithm Input and Output Data Definition (IODD)


### Input data

```{table} Input Data
:name: InData
| Parameter  | Description  | Shape |
|------------|--------------|-------|
| L1B TB      | L1B Brightness Temperature at L, C and X-bands <br> ( H and V polarization) | Full swath or swath section <br> (Nscans, Npos) |
| L1B NeΔT | Random radiometric uncertainty of the channels | Full swath or swath section <br> (Nscans, Npos) |
```

### Output data

```{table} Output Data
:name: OutData
| Parameter | Description | Units | Shape |
|-----------|-------------|-------|-------|
| lon | Longitude [0$^{\circ}$, 360$^{\circ}$] | *deg East* | EASE2 grid <br> (nx,ny) |
| lat | Latitude [90$^{\circ}$S, 90$^{\circ}$N] | *deg North* | EASE2 grid <br> (nx,ny) |
| time | Sensing time of L-band | *ms* | EASE2 grid <br> (nx,ny) |
| TB_L | L1b Brightness Temperature at L-band | *K* | EASE2 grid <br> (nx,ny) |
| TB_L_E | L1b Enhanced Brightness Temperature at L-band | *K* | EASE2 grid <br> (nx,ny) |
| SM | Soil Moisture | *m$^{3}$/m$^{3}$* | EASE2 grid <br> (nx,ny) |
| SM_E | Enhanced Soil Moisture | *m$^{3}$/m$^{3}$* | EASE2 grid <br> (nx,ny) |
| VOD  | Vegetation Optical Depth | - | EASE2 grid <br> (nx,ny) |
| VOD_E  | Enhanced Vegetation Optical Depth | - | EASE2 grid <br> (nx,ny) |
| albedo | Vegetation single scattering albedo | - | EASE2 grid <br> (nx,ny) |
| EASE row index | Row index in EASE2 grid | - | EASE2 grid <br> (nx,ny) |
| EASE column index | Column index in EASE2 grid | - | EASE2 grid <br> (nx,ny) |
| TB_L_RMSE | RMSE between measured and modeled TB | *K* | EASE2 grid <br> (nx,ny) |
| TB_L_E_RMSE | RMSE between enhanced and modeled TB | *K* | EASE2 grid <br> (nx,ny) |
| scene_flags | Flag to indicate difficult inversion situations | *8-bit flag* | EASE2 grid <br> (nx,ny) |
| status_flag | Product quality flag | *n/a* | EASE2 grid <br> (nx,ny) |
```

### Auxiliary data

```{table} Auxiliary data
:name: AuxData
| Parameter  | Description  | Shape |
|------------|--------------|-------|
| LST   | Land Surface Temperature  (from ECMWF)  |  EASE2 grid <br> (nx,ny) |
| CIMR_LST   | CIMR Land Surface Temperature  |  EASE2 grid <br> (nx,ny) |
| soil_texture   | Clay fraction (from FAO)     |  EASE2 grid <br> (nx,ny) |
| LCC   | Land Cover type Classification |   EASE2 grid <br> (nx,ny) |
| albedo  | Vegetation single scattering albedo (from SMOS-IC)  |  EASE2 grid <br> (nx,ny) |
| H   | Surface roughness information (from SMOS-IC)  |  EASE2 grid <br> (nx,ny) |
| DEM  | Digital Elevation Model     | EASE2 grid <br> (nx,ny) |
| hydrology_mask  | CIMR Hydrology Target mask ({doc}`[RD-1] <applicable_ref_docs>`, MRD-854) |  EASE2 grid <br> (nx,ny) |
```
