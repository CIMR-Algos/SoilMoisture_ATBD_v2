# Algorithm Input and Output Data Definition (IODD)


### Input data

```{table} Input Data
:name: InpData
| Parameter   | Description                                                                 | Shape                     |
|-------------|-----------------------------------------------------------------------------|---------------------------|
| L1B TB      | L1B Brightness Temperature at L, C and X-bands (both H and V polarization) | *Full swath or swath section (Nscans, Npos)* |
| L1B NeΔT | Random radiometric uncertainty of the channels | *Full swath or swath section (Nscans, Npos)* |
```

### Output data

```{table} Output Data
:name: OutData
| Parameter          | Description                                      | Units     | Shape                          |
|--------------------|--------------------------------------------------|-----------|-------------------------------------|
| lon | Longitude [0$^{\circ}$, 360$^{\circ}$] | *deg East* | L1c |
| lat | Latitude [90$^{\circ}$S, 90$^{\circ}$N] | *deg North* | L1c |
| time | seconds since YYYY-MM-DD 00:00:00 UTC | *seconds* | L1c |
| TB_L | L1b Brightness Temperature at L-band | *K* | L1c |
| TB_L_E | L1b Enhanced Brightness Temperature at L-band | *K* | L1c |
| SM | Soil Moisture | *m$^{3}$/m$^{3}$* | L1c |
| SM_E | Enhanced Soil Moisture | *m$^{3}$/m$^{3}$* | L1c |
| VOD  | Vegetation Optical Depth | - | L1c |
| VOD_E  | Enhanced Vegetation Optical Depth | - | L1c |
| albedo | Vegetation single scattering albedo | - | L1c |
| EASE row index | Row index in EASE2 grid | - | L1c |
| EASE column index | Column index in EASE2 grid | - | L1c |
| TB_L_RMSE | RMSE between measured and modeled TB | *K* | L1c |
| TB_L_E_RMSE | RMSE between enhanced and modeled TB | *K* | L1c |
| scene_flags | Flag to indicate difficult inversion situations | *8-bit flag* | L1c |
| status_flag | Product quality flag | *n/a* | L1c |
```

### Ancillary data

```{table} Ancillary data
:name: AncData
| Parameter                               | Description                                         | Shape               |
|-----------------------------------------|-----------------------------------------------------|----------------------------|
| CIMR_SWF                     | CIMR Surface Water Fraction  |  L1c |
| CIMR_LST                     | CIMR Land Surface Temperature  |  L1c |
| LST                     | Land Surface Temperature  (from ECMWF)  |  L1c |
| soil_texture            | Clay fraction (from FAO)     |  L1c |
| LCC          | Land Cover type Classification |   L1c |
| albedo     | Vegetation single scattering albedo (from SMOS-IC)  |  L1c |
| H           | Surface roughness information   |  L1c |
| DEM                  | Digital Elevation Model     | L1c |
| hydrology_mask         | CIMR Hydrology Target mask ({doc}`[RD-1] <applicable_ref_docs>`, MRD-854) |  L1c |
```
