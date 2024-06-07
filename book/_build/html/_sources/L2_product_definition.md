# Level-2 product definition

```{table} L2-product
:name: L2product
| Parameter                 | Description                                                | Units     | Dimensions                      |
|---------------------------|------------------------------------------------------------|-----------|---------------------------------|
| lon | Longitude [0$^{\circ}$, 360$^{\circ}$] | *deg East* | *(xdim$_{grid}$, ydim$_{grid}$)* |
| lat | Latitude [90$^{\circ}$S, 90$^{\circ}$N] | *deg North* | *(xdim$_{grid}$, ydim$_{grid}$)* |
| time     | seconds since YYYY-MM-DD 00:00:00 UTC | *seconds* | *(xdim$_{grid}$, ydim$_{grid}$)* |
| TB_L             | L1b Brightness Temp at L-band | *K* | *(xdim$_{grid}$, ydim$_{grid}$)* |
| TB_L_E             | L1b Enhanced Temp at L-band | *K* | *(xdim$_{grid}$, ydim$_{grid}$)* |
| SM             | Soil Moisture | *m$^{3}$/m$^{3}$* | *(xdim$_{grid}$, ydim$_{grid}$)* |
| SM_E             | Enhanced Soil Moisture | *m$^{3}$/m$^{3}$* | *(xdim$_{grid}$, ydim$_{grid}$)* |
| VOD  | Veg Optical Depth | - | *(xdim$_{grid}$, ydim$_{grid}$)* |
| VOD_E  | Enhanced Veg Optical Depth | - | *(xdim$_{grid}$, ydim$_{grid}$)* |
| albedo    | Veg single scattering albedo | - | *(xdim$_{grid}$, ydim$_{grid}$)* |
| EASE row index  | Row index in EASE2 grid | - | *(xdim$_{grid}$, ydim$_{grid}$)* |
| EASE column index | Column index in EASE2 grid | - | *(xdim$_{grid}$, ydim$_{grid}$)* |
| TB_L_RMSE | RMSE between measured and modeled TB | *K* | *(xdim$_{grid}$, ydim$_{grid}$)* |
| TB_L_E_RMSE | RMSE between enhanced and modeled TB | *K* | *(xdim$_{grid}$, ydim$_{grid}$)* |
| scene_flags | RFI, proximity to water body, etc. | *8-bit flag* | *(xdim$_{grid}$, ydim$_{grid}$)* |
| status_flag | Product quality flag | *n/a* | *(xdim$_{grid}$, ydim$_{grid}$)* |
```