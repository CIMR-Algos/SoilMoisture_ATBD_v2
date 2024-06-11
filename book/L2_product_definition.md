# Level-2 product definition

```{table} Level-2 Soil Moisture product (36 km grid)
:name: L2product
| Parameter                 | Description                                                | Units     | Dimensions                      |
|---------------------------|------------------------------------------------------------|-----------|---------------------------------|
| time     | Time of observation | *seconds* | (964, 406) |
| EASE row index  | Row index in EASE2 global 36 km grid | - | (964, 406) |
| EASE column index | Column index in EASE2 global 36 km grid | - | (964, 406) |
| lon | Longitude [0$^{\circ}$, 360$^{\circ}$] | *deg East* | (964, 406) |
| lat | Latitude [90$^{\circ}$S, 90$^{\circ}$N] | *deg North* | (964, 406) |
| SM             | Soil Moisture | *m$^{3}$/m$^{3}$* | (964, 406) |
| VOD  | Vegetation Optical Depth | - | (964, 406) |
| TB_L             | Gridded L-band TB | *K* | (964, 406) |
| TB_L_RMSE | RMSE between measured and modeled TB | *K* | (964, 406) |
| scene_flags | Flag to indicate difficult inversion situations | *8-bit flag* | (964, 406) |
| status_flag | Product quality flag | *n/a* | (964, 406) |
```

```{table} Level-2 enhanced Soil Moisture product (9 km grid)
:name: L2product
| Parameter                 | Description                                                | Units     | Dimensions                      |
|---------------------------|------------------------------------------------------------|-----------|---------------------------------|
| time     | Time of observation | *seconds* | (3856, 1624) |
| EASE row index  | Row index in EASE2 global 9 km grid | - | (3856, 1624) |
| EASE column index | Column index in EASE2 global 9 km grid | - | (3856, 1624) |
| lon | Longitude [0$^{\circ}$, 360$^{\circ}$] | *deg East* | (3856, 1624) |
| lat | Latitude [90$^{\circ}$S, 90$^{\circ}$N] | *deg North* | (3856, 1624) |
| SM_E             | Enhanced Soil Moisture | *m$^{3}$/m$^{3}$* | (3856, 1624) |
| VOD_E  | Enhanced Vegetation Optical Depth | - | (3856, 1624) |
| TB_L_E             | Gridded L-band TB | *K* | (3856, 1624) |
| TB_L_E_RMSE | RMSE between enhanced and modeled TB | *K* | (3856, 1624) |
| scene_flags | Flag to indicate difficult inversion situations | *8-bit flag* | (3856, 1624) |
| status_flag | Product quality flag | *n/a* | (3856, 1624) |
```