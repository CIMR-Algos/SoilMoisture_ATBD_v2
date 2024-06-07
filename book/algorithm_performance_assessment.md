# Algorithm Performance Assessment

This chapter presents a performance assessment of the prototype soil moisture retrieval algorithm based on end-to-end simulations of a synthetic reference scenario. The full python code used in the algorithm and evaluation can be found in the [SM_ATBD_v2 Github Repository](https://github.com/CIMR-Algos/SoilMoisture_ATBD_v2/tree/main/algorithm).

## L1 E2ES Demonstration Reference Scenario (Picasso) scene definition

A synthetic soil moisture test card was created to serve as a testbed for the soil moisture retrieval algorithm.

The test card has a spatial resolution of 1 km, which is nested within the global 9 km and 36 km EASE2 grids. At L-, C-, and X-bands, the brightness temperature signatures of the test card are based on numerical simulations of a discrete radiative transfer model (Tor Vergata model) {cite:p}`ferrazzoli2002simulating,guerriero2016band`. At Ku- and Ka-bands, brightness temperature signatures are based on forward simulations of the tau-omega model (not used in this prototype) {cite:p}`Mo1982`. Five land use classes are considered: Bare soil, grassland, cropland, mixed, and forest. The mixed class assumes an homogeneous mix of grassland, cropland, and forest.

```{figure} /images/algo_fig1.png
--- 
name: algo_fig1
---
Synthetic soil moisture test card at 1 km (upper, native resolution), 9 km (middle, aggregated) and 36 km (lower, aggregated). Columns indicate the dominant land use, average soil moisture content, and L-band brightness temperatures at V- and H-polarization, respectively. Brightness temperatures at C-, X-, Ku-, Ka-bands are not shown for brevity.
```

{numref}`algo_fig1` shows the synthetic test card for 1 km (native resolution), 9 km, and 36 km resolutions. The soil moisture fields at 9 km and 36 km resolutions will be used as a reference for the performance evaluation. Four areas of interest (AOIs) are indicated by black boxes. These areas indicate four distinct land use classes that contain identical soil moisture patterns.

## Algorithm Performance Metrics (MPEF)

Two algorithm performance metrics are used in the evaluation: The unbiased root mean squared error (ubRMSE) and the bias of soil moisture retrievals with respect to the synthetic reference.

We test the prototype algorithm on four simulated L1B files, which represent distinct CIMR overpasses over the synthetic test card. The L1B files are based on orbit simulations conducted by DEIMOS and the SCEPS project. Each orbit simulator covers one ascending and descending orbit, respectively, leading to a total of four synthetic CIMR L1B files. 

## Test Results using Demonstration Reference Scenario

### Regridding

The purpose of regridding is to move from L1B TB signatures, provided in swath geometry, to gridded TB signatures, posted on a global EASE2 grid. In a first step, we grid L-band TBs to the 36 km global EASE2 grid, using a Gaussian regridding (Note: More advanced gridding techniques, such as the Backus-Gilbert optimal interpolation technique, are planned to be implemented in a separate toolbox). In a second step, we sharpen the gridded L-band TBs to the 9 km EASE2 grid. The sharpening is achieved by applying the smoothing filter-based intensity modulation technique (SFIM) {cite:p}`Santi2010`, using L-band TBs at the 36 km grid and C-band TBs at the 36 km and 9 km grids as inputs. 

$$ 
TB_L(9 km) = \frac{TB_L(36 km)}{TB_C(36 km)} TB_C(9 km).
$$

Should C-band TBs be affected by radio frequency interference (RFI), the same technique can also be applied using X-band TBs, leading to comparable results (not shown). 

```{figure} /images/algo_fig2.png
--- 
name: algo_fig2
---
L-band brightness temperature signatures posted on a 36 km global EASE2 grid. 
```

```{figure} /images/algo_fig3.png
--- 
name: algo_fig3
---
L-band brightness temperature signatures (sharpened with C-band) posted on a 9 km global EASE2 grid.
```

### Soil Moisture Retrieval Results

We apply the prototype soil moisture retrieval algorithm the gridded L-band TB signatures at 36 km and 9 km. The results are shown in {numref}`algo_fig4` and {numref}`algo_fig5`, respectively. In addition to soil moisture retrievals, we also show outputs for vegetation optical depth (VOD), noting that VOD is not a target variable of the algorithm and will not be subject to performance evaluation. We find that soil moisture patterns are captured well across all land use types. VOD retrievals correspond to expected patterns of different land use classes, noting that cropland and grassland are almost transparent at L-band for the test card scenario considered here. A more detailed assessment of the results is given in the next section.

```{figure} /images/algo_fig4.png
--- 
name: algo_fig4
---
Soil moisture and vegetation optical depth (VOD) retrieval results of the prototype algorithm at the 36 km resolution. The results are based on gridded L-band TBs. 
```

```{figure} /images/algo_fig5.png
--- 
name: algo_fig5
---
Soil moisture and vegetation optical depth (VOD) retrieval results of the prototype algorithm at the 9 km resolution. The results are based on gridded L-band TBs that are sharpened by means of higher resolution C-band TBs. 
```

## Algorithm Performance Assessment using Demonstration Reference Scenario

We evaluate the prototype algorithm retrievals against the synthetic reference in {numref}`algo_fig6` and {numref}`algo_fig7`. Several observations can be made:
- Errors within the AOIs (black boxes) are generally low, indicating that soil moisture patterns are captured across different land use classes. 
- The largest errors occur at coastlines, which is expected due to spillover effects of waterbody TB signatures.
- Biases occur for forest regions, which is expected given the dense vegetation.
- DEIMOS scenes show enhanced errors at the top and left corner of the scene. These errors are related to spillover effects of the background field used in the L1B orbit simulations and are not related to the algorithm or processing steps.
- SCEPS scenes show effects of instrument noise (not considered in DEIMOS), which is particularly visible for forest retrievals.
- Barring minor differences across orbit simulators, the retrieval results are consistent across overpasses.

Two additional observations apply only to 9 km retievals: First, vertical edge effects are visible in the northeastern corner of the test card, which is an artifact resulting from the sharp land cover transitions in the synthetic test card. Second, note that the 9 km retrievals are evaluated against 9 km soil moisture patterns, such that additional error patterns are visible within the AOIs compared to 36 km retrievals. A more detailed view of these patterns is given in {numref}`algo_fig8`.

```{figure} /images/algo_fig6.png
--- 
name: algo_fig6
---
Soil moisture retrieval results of the prototype algorithm at the 36 km resolution (based on L-band TBs, upper row). Errors with respect to the synthetic reference, aggregated to the same resolution (middle row). Retrieval scene flags that indicate uncertain retrievals (lower row).
```

```{figure} /images/algo_fig7.png
--- 
name: algo_fig7
---
Soil moisture retrieval results of the prototype algorithm at the 9 km resolution (based on L-band and C-band TBs, upper row). Errors with respect to the synthetic reference, aggregated to the same resolution (middle row). Retrieval scene flags that indicate uncertain retrievals (lower row).
```

A more detailed view of the 9 km retrievals is given in {numref}`algo_fig8`. We compare the soil moisture reference at 9 km grid (left row) with L2 retrievals at the 36 km (middle row) and 9 km (right row) grids. This aims to illustrate the added value of 9 km retrievals compared to 36 km retrievals, assuming reference soil moisture patterns at 9 km resolution.

As expected, 9 km retrievals generally improve the representation of soil moisture patterns at the 9 km scale (compared to retrievals at 36 km). The improvement is particularly pronounced for bare soil (bottom right AOI) and grassland (top right AOI). This is expected as the C-band signal from the soil gets increasingly masked with increasing vegetation cover. Comparable results are obtained for X-band signals (not shown). Note that the synthetic test card assessed here does not show spatial land cover variability at the 9 km scale, which limits the available brightness temperature variability to be captured by the sharpening algorithm. It is expected that the added value of the sharpening would increase further for scenes that include spatial land cover heterogeneity.


```{figure} /images/algo_fig8.png
--- 
name: algo_fig8
---
Detailed view of 9 km retrievals compared to 36 km retrievals. Errors are computed based on reference soil moisture patterns aggregated to the 9 km grid.
```

Finally, ubRMSE and bias metrics are displayed in {numref}`algo_fig9` and {numref}`algo_fig10`. The metrics are calculated for identical soil moisture patterns retrieved over four land use classes: Bare soil, grassland, cropland, and mixed. These classes correspond to vegetation water content (VWC) values of 0 kg/m², 0.2 kg/m², 2.0 kg/m², 4.6 kg/m², respectively. Forest regions show a vegetation water content of 11.7 kg/m² and are not considered in the evaluation. The exact areas of interest (AOIs) over which the metrics are computed are indicated in black boxes in {numref}`algo_fig4` to {numref}`algo_fig8`. 


```{figure} /images/algo_fig9.png
--- 
name: algo_fig9
---
ubRMSE and bias metrics for soil moisture retrievals at the 36 km scale.
```

```{figure} /images/algo_fig10.png
--- 
name: algo_fig10
---
ubRMSE and bias metrics for soil moisture retrievals at the 9 km scale.
```

We summarize the results of the performance evaluation below:
- At the 36 km scale, the algorithm shows an ubRMSE < 0.04 m³/m³.
- At the 9 km scale, the algorithm shows an ubRMSE between 0.035-0.045 m³/m³. 
- Errors generally increase with increasing vegetation cover, in accordance with expectations.
- Biases are overall low.
- The results are consistent across overpasses. 

**Noting that the algorithm parameters have not been calibrated prior to the evaluation, the results provide a promising outlook on the prototype SM retrieval algorithm for CIMR.**


# Roadmap for future ATBD development

For the development of future versions of the ATBD, one of the focus will be the global calibration of soil roughness across L-, C-, and X-bands. This new calibration will be assessed against the existing calibration based on the SMOS-IC retrieval algorithm {cite:p}`fernandez-moran2017`. The use of CIMR's higher frequency bands for estimating land surface temperature, necessary as an input in the SM algorithm, will be under study. Ka/Ku bands will serve this purpose ({cite:p}`holmes2009,prigent2016toward,jimenez2017inversion`). CIMR land surface temperature retrievals will be tested against the use of ERA5 skin and soil temperatures, which are established as the primary temperature ancillary datasets.

To meet the needs of global hydro climatology (~60 km, daily) and hydrometeorology (~15 km, daily), the algorithm will produce two soil moisture products: A single-frequency SM product at the <60 km scale based on L-band TB measurements and a multi-frequency SM product at the <15 km scale by sharpening L-band measurements with higher resolution C-/X-band data. Preliminary studies, such as {cite:p}`Zhang2024`, have demonstrated the global applicability of C-band for L-band disaggregation. Techniques like the smoothing filter-based intensity modulation (SFIM) ({cite:p}`Santi2010`) will be central to this process.

For estimating microwave vegetation indices (MMVI), the SM product at <15 km scale may serve as an initial guess to invert the tau-omega model and estimate time-dynamic VOD and ω from CIMR L-, C-, and X-bands (following the work of {cite:p}`Baur2021`, at L-band). These microwave vegetation parameters represent the absorption and scattering properties of microwaves at different canopy depths, which are deeper at lower frequencies. This allows capturing interactions between various wavelengths and canopy components such as branches, stems, and leaves, relating to significant vegetation characteristics like vegetation water content and above-ground biomass.
