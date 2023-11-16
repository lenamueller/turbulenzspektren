
from Datasets import ExpeDataset, SonicDataset
from setup import metadata


def save_spectrum(puo: str, measuring_device: str) -> None:
    """This script saves the spectra data of a given measuring device and
    period under observation to a .csv file to data/spectra_data/."""

    # create Dataset objects
    expe_fn, sonic_fn, start_date, end_date, _, _ = metadata(puo)

    if measuring_device == "SONIC":
        ds = SonicDataset(fn=sonic_fn, start_time=start_date, end_time=end_date)
    elif measuring_device == "EXPE":
        ds = ExpeDataset(fn=expe_fn, start_time=start_date, end_time=end_date)
    else:
        raise ValueError("measuring_device must be 'SONIC' or 'EXPE'")

    # save data
    ds.save_spectrum_data(puo=puo)