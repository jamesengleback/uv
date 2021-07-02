# `uv`

Some tools for UV-Vis spectroscopy analysis for data from a *Varian* spectrometer. Oriented towards P450s

## background

## features

Spectroscopy data from *Varian* spectrometers (`csv`) requires some data cleaning, which is handled in the `uv.Data` class, which returns a clean `pandas` DataFrame with the `.df` property.

For P450 UV-Vis spectroscopy, there is a `P450` subclass of `Data` with the additional features:

- `__init__(self, path, extinction_coef=None)` an extinction coefficient can be supplied for calculating the P450 concentraion based on its absorbance at 420 nm.
- `norm` (property) - zero all traces at 800 nm and subtractes the buffer blank (assuming that's the first trace, which is usually the case)
- `concs` (property should it be?) - 
- `norm800` (method, no args) - used by `norm`, zero all traces at 800 nm
- `baselineCorr` (method, no args)

The `BM3` object subclasses from `P450` except with the extiction coefficient (95 for the P450 BM3 heme domain) supplied.


Extra bits:
- `uv.plot_traces(df, title = '')` which plots the traces from a `uv.Data.df` instance.
- `uv.calc_change_a420_a390(x)`
- `r_squared(yi,yj)`
- `MichaelisMenten(x, y)`



## how to
