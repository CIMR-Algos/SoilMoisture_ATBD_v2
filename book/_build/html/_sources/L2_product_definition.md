# Level-2 product definition

The following is an initial proposal for a CIMR L2 soil moisture product structure. Two L2 products are envisioned: One based on L-band TBs at their native resolution and one based on L-band TBs sharpened with C-/X-band TBs for an enhanced resolution. 

The main content of the L2 files are the gridded soil moisture and vegetation optical depth fields. Scene and status flags provide information about the quality and status of the retrieval, respectively. For this prototype implementation, the gridded brightness temperature fields and the RMSE between measured and modelled brightness temperatures are provided as additional output.


```{table} Level-2 Soil Moisture product (36 km grid)
:name: L2product36km
| Parameter                 | Description                                                | Units     | Dimensions*                     |
|---------------------------|------------------------------------------------------------|-----------|---------------------------------|
| time     | Time of observation | *seconds* | (964, 406) |
| EASE row index  | Row index in EASE2 grid | - | (964, 406) |
| EASE column index | Column index in EASE2 grid | - | (964, 406) |
| lon | Longitude [0$^{\circ}$, 360$^{\circ}$] | *deg East* | (964, 406) |
| lat | Latitude [90$^{\circ}$S, 90$^{\circ}$N] | *deg North* | (964, 406) |
| SM             | Soil Moisture | *m$^{3}$/m$^{3}$* | (964, 406) |
| VOD  | Vegetation Optical Depth | - | (964, 406) |
| scene_flags | Flag to indicate difficult inversion situations | *8-bit flag* | (964, 406) |
| status_flag | Product quality flag | *n/a* | (964, 406) |
| TBV_L | Gridded L-band TBV | *K* | (964, 406) |
| TBH_L | Gridded L-band TBH | *K* | (964, 406) |
| TB_L_RMSE | RMSE between measured and modeled TB | *K* | (964, 406) |

```

```{table} Level-2 enhanced Soil Moisture product (9 km grid)
:name: L2product9km
| Parameter                 | Description                                                | Units     | Dimensions*                     |
|---------------------------|------------------------------------------------------------|-----------|---------------------------------|
| time     | Time of observation | *seconds* | (3856, 1624) |
| EASE row index  | Row index in EASE2 grid | - | (3856, 1624) |
| EASE column index | Column index in EASE2 grid | - | (3856, 1624) |
| lon | Longitude [0$^{\circ}$, 360$^{\circ}$] | *deg East* | (3856, 1624) |
| lat | Latitude [90$^{\circ}$S, 90$^{\circ}$N] | *deg North* | (3856, 1624) |
| SM_E             | Enhanced Soil Moisture | *m$^{3}$/m$^{3}$* | (3856, 1624) |
| VOD_E  | Enhanced Vegetation Optical Depth | - | (3856, 1624) |
| scene_flags | Flag to indicate difficult inversion situations | *8-bit flag* | (3856, 1624) |
| status_flag | Product quality flag | *n/a* | (3856, 1624) |
| TBV_L_E | Gridded enhanced L-band TBV | *K* | (3856, 1624) |
| TBH_L_E | Gridded enhanced L-band TBH | *K* | (3856, 1624) |
| TB_L_E_RMSE | RMSE between enhanced and modeled TB | *K* | (3856, 1624) |
```


\* Dimensions are equivalent to the global EASE2 grids at 36 km and 9 km resolution, respectively. 
This is the initial proposal for CIMR soil moisture retrievals and corresponds to 
the current implementation in the later sections of this ATBD. 
The final grid resolution will be decided based on further tests on the tradeoff between noise and spatial resolution.