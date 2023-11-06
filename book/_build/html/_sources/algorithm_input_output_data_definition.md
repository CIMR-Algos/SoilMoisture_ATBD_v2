# Algorithm Input and Output Data Definition (IODD)


### Input data

```{table} Input Data
:name: InpData
| Parameter   | Description                                                                 | Shape/Amount                      |
|-------------|-----------------------------------------------------------------------------|----------------------------------|
| L1B TB      | L1B Brightness Temperature at L, C and X-bands (both H and V polarization) | *Full swath or swath section (Nscans, Npos)* |
| L1B NeΔT | Random radiometric uncertainty of the channels | *Full swath or swath section (Nscans, Npos)* |
```

### Output data

```{table} Output Data
:name: OutData
:name: OutData
| Parameter                 | Description                                                | Units     | Dimensions                      |
|---------------------------|------------------------------------------------------------|-----------|---------------------------------|
| lon | Longitude [0$^{\circ}$, 360$^{\circ}$] | *deg East* | *(xdim$_{grid}$, ydim$_{grid}$)* |
| lat | Latitude [90$^{\circ}$S, 90$^{\circ}$N] | *deg North* | *(xdim$_{grid}$, ydim$_{grid}$)* |
| time     | seconds since YYYY-MM-DD 00:00:00 UTC | *seconds* | *(xdim$_{grid}$, ydim$_{grid}$)* |
| TB_L             | L1b Brightness Temperature at L-band | *K* | *(xdim$_{grid}$, ydim$_{grid}$)* |
| TB_L_E             | L1b Enhanced Brightness Temperature at L-band | *K* | *(xdim$_{grid}$, ydim$_{grid}$)* |
| SM             | Soil Moisture | *m$^{3}$/m$^{3}$* | *(xdim$_{grid}$, ydim$_{grid}$)* |
| SM_E             | Enhanced Soil Moisture | *m$^{3}$/m$^{3}$* | *(xdim$_{grid}$, ydim$_{grid}$)* |
| VOD  | Vegetation Optical Depth | - | *(xdim$_{grid}$, ydim$_{grid}$)* |
| VOD_E  | Enhanced Vegetation Optical Depth | - | *(xdim$_{grid}$, ydim$_{grid}$)* |
| albedo    | Vegetation single scattering albedo | - | *(xdim$_{grid}$, ydim$_{grid}$)* |
| EASE row index  | Row index in EASE2 grid | - | *(xdim$_{grid}$, ydim$_{grid}$)* |
| EASE column index | Column index in EASE2 grid | - | *(xdim$_{grid}$, ydim$_{grid}$)* |
| TB_L_RMSE | RMSE between measured and modeled TB | *K* | *(xdim$_{grid}$, ydim$_{grid}$)* |
| TB_L_E_RMSE | RMSE between enhanced and modeled TB | *K* | *(xdim$_{grid}$, ydim$_{grid}$)* |
| scene_flags | Flag to indicate difficult inversion situations | *8-bit flag* | *(xdim$_{grid}$, ydim$_{grid}$)* |
| status_flag | Product quality flag | *n/a* | *(xdim$_{grid}$, ydim$_{grid}$)* |
```

### Ancillary data

```{table} Ancillary data
:name: AncData
| Parameter                               | Description                                         | Shape/Amount               |
|-----------------------------------------|-----------------------------------------------------|----------------------------|
| CIMR_SWF                     | CIMR Surface Water Fraction  |  *(xdim$_{grid}$, ydim$_{grid}$)* |
| CIMR_LST                     | CIMR Land Surface Temperature  |  *(xdim$_{grid}$, ydim$_{grid}$)* |
| LST                     | Land Surface Temperature  (from ECMWF)  |  *(xdim$_{grid}$, ydim$_{grid}$)* |
| soil_texture            | Clay fraction (from FAO)     |  *(xdim$_{grid}$, ydim$_{grid}$)* |
| LCC          | IGBP Land Cover type Classification (from MODIS) |   *(17, xdim$_{grid}$, ydim$_{grid}$)* |
| albedo     | Vegetation single scattering albedo (from SMOS-IC)  |  *(xdim$_{grid}$, ydim$_{grid}$)* |
| H           | Surface roughness information (from SMOS-IC)   |  *(xdim$_{grid}$, ydim$_{grid}$)* |
| DEM                  | Digital Elevation Model     | *(xdim$_{grid}$, ydim$_{grid}$)* |
| hydrology_mask                     | CIMR Hydrology Target mask ([RD-1, MRD-854]) |  *(xdim$_{grid}$, ydim$_{grid}$)* |
```
