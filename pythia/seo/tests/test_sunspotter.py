from pathlib import Path

import astropy.units as u
import numpy as np
import pandas as pd
import pytest
from astropy.coordinates import Angle, Latitude, Longitude
from pythia.seo.sunspotter import Sunspotter
from sunpy.util import SunpyUserWarning

path = Path.cwd() / "data/all_clear"


@pytest.fixture
def properties_columns():
    return ['#id', 'filename', 'zooniverse_id', 'angle', 'area', 'areafrac',
            'areathesh', 'bipolesep', 'c1flr24hr', 'id_filename', 'flux',
            'fluxfrac', 'hale', 'hcpos_x', 'hcpos_y', 'm1flr12hr', 'm5flr12hr',
            'n_nar', 'noaa', 'pxpos_x', 'pxpos_y', 'sszn', 'zurich']


@pytest.fixture
def properties(properties_columns):
    # Properties corresponding to `obs_date` '2000-01-01 12:47:02' and `#id` 1
    data = [[1, '530be1183ae74079c300000d.jpg', 'ASZ000090y', 37.8021,
             34400.0, 0.12, 2890.0, 3.72, 0, 1, 2.18e+22, 0.01, 'beta', 452.26991,
             443.92976, 0, 0, 1, 8809, 229.19343999999998, 166.877, 1, 'bxo']]

    return pd.DataFrame(data=data, columns=properties_columns)


@pytest.fixture
def timesfits_columns():
    return ['#id', 'filename', 'obs_date']


@pytest.fixture
def timesfits_csv():
    return pd.read_csv(path / "lookup_timesfits.csv", delimiter=';')


@pytest.fixture
def properties_csv():
    return pd.read_csv(path / "lookup_properties.csv", delimiter=';')


@pytest.fixture
def classifications_columns():
    return ['#id', 'zooniverse_class', 'user_id', 'image_id_0', 'image_id_1',
            'image0_more_complex_image1', 'used_inverted', 'bin', 'date_created',
            'date_started', 'date_finished']


@pytest.fixture
def rankings_columns():
    return ['#id','image_id', 'count', 'k_value', 'score', 'std_dev']


@pytest.fixture
def sunspotter(properties_columns, timesfits_columns, classifications_columns, rankings_columns):
    return Sunspotter(timesfits=path / "lookup_timesfits.csv",
                      properties=path / "lookup_properties.csv",
                      classifications=path / "classifications.csv",
                      rankings=path/ "rankings.csv",
                      delimiter=';',
                      timesfits_columns=timesfits_columns,
                      properties_columns=properties_columns,
                      classifications_columns=classifications_columns,
                      rankings_columns=rankings_columns)


@pytest.fixture
def obsdate():
    # `obs_date` corresponding to `#id` 1
    return '2000-01-01 12:47:02'


@pytest.fixture
def comparision_df():
    df = pd.DataFrame(columns=['id_filename', 'Sunspotter NOAA', 'HEK NOAA', 'Sunspotter Longitude',
                               'HEK Longitude', 'Sunspotter Latitude', 'HEK Latitude'])
    df['id_filename'] = [12961, 12962, 12963, 12964, 12965]
    df['Sunspotter NOAA'] = [10838, 10840, 10841, 10843, 10844]
    df['HEK NOAA'] = [10838, 10840, 10841, 10843, 10844]
    df['Sunspotter Longitude'] = [75.80890071046657, 18.19194752908415,
                                  11.644637399338993, -7.105893517350921, 76.8112979233762]
    df['HEK Longitude'] = [88, 26, 16, -2, 81]
    df['Sunspotter Latitude'] = [16.218928298804492, -2.875432955561788,
                                 11.521982686891043, 12.301116578845914, -14.756412258758138]
    df['HEK Latitude'] = [15, -3, 12, 12, -14]
    df.set_index(keys=['id_filename'], inplace=True)
    return df


def test_sunspotter_no_parameters():
    timesfits = pd.read_csv(path / "lookup_timesfits.csv", delimiter=';')
    properties = pd.read_csv(path / "lookup_properties.csv", delimiter=';')

    # get all columns is by default True for both Timesfits and Properties.
    sunspotter = Sunspotter()

    # To get obs_date back a column of dtype `str`
    sunspotter.timesfits.reset_index(inplace=True)
    sunspotter.timesfits.obs_date = sunspotter.timesfits.obs_date.dt.strftime(
        '%Y-%m-%d %H:%M:%S')

    # To get #id back a column of dtype int
    sunspotter.properties.reset_index(inplace=True)

    # Sorting columns as the order of Columns shouldn't matter
    assert sunspotter.timesfits.sort_index(
        axis=1).equals(timesfits.sort_index(axis=1))
    assert sunspotter.properties.sort_index(
        axis=1).equals(properties.sort_index(axis=1))


def test_sunspotter_base_object(properties_columns, timesfits_columns):

    sunspotter = Sunspotter(timesfits=path / "lookup_timesfits.csv",
                            properties=path / "lookup_properties.csv",
                            timesfits_columns=timesfits_columns,
                            properties_columns=properties_columns)

    assert set(sunspotter.properties_columns) == set(properties_columns)
    assert set(sunspotter.timesfits_columns) == set(timesfits_columns)


def test_sunspotter_with_classifications(classifications_columns):

    sunspotter = Sunspotter()

    assert sunspotter.classifications_columns is None
    assert sunspotter.classifications is None

    with pytest.raises(SunpyUserWarning):
        # Because Classifications Columns aren't specified.
        Sunspotter(classifications=path / "classifications.csv")

    sunspotter = Sunspotter(classifications=path / "classifications.csv",
                            classifications_columns=classifications_columns)

    assert set(sunspotter.classifications_columns) == set(
        classifications_columns)


def test_sunspotter_with_rankings(rankings_columns):

    sunspotter = Sunspotter()

    assert sunspotter.rankings_columns is None
    assert sunspotter.rankings is None

    with pytest.raises(SunpyUserWarning):
        # Because Rankings Columns aren't specified.
        Sunspotter(rankings=path / "rankings.csv")

    sunspotter = Sunspotter(rankings=path / "rankings.csv",
                            rankings_columns=rankings_columns)

    assert set(sunspotter.rankings_columns) == set(rankings_columns)


def test_sunspotter_incorrect_delimiter():

    with pytest.raises(SunpyUserWarning):
        Sunspotter(timesfits=path / "lookup_timesfits.csv",
                   properties=path / "lookup_properties.csv",
                   delimiter=',')


def test_sunspotter_properties_columns():

    with pytest.raises(SunpyUserWarning):
        Sunspotter(timesfits=path / "lookup_timesfits.csv",
                   properties=path / "lookup_properties.csv",
                   properties_columns=["This shouldn't be present"],
                   delimiter=';')


def test_sunspotter_classifications_columns():

    with pytest.raises(SunpyUserWarning):
        Sunspotter(timesfits=path / "lookup_timesfits.csv",
                   properties=path / "lookup_properties.csv",
                   classifications=path / "classifications.csv",
                   classifications_columns=["This shouldn't be present"],
                   delimiter=';')


def test_sunspotter_timesfits_columns():

    with pytest.raises(SunpyUserWarning):
        Sunspotter(timesfits=path / "lookup_timesfits.csv",
                   properties=path / "lookup_properties.csv",
                   timesfits_columns=["This shouldn't be present"],
                   delimiter=';')


def test_get_timesfits_id(sunspotter, obsdate):
    assert sunspotter.get_timesfits_id(obsdate) == 1


def test_get_all_ids_for_observation(sunspotter, obsdate):

    assert all(sunspotter.get_all_ids_for_observation(
        obsdate) == np.array([1, 2, 3, 4, 5]))


def test_get_properties(sunspotter, properties):
    properties.set_index("id_filename", inplace=True)
    assert sunspotter.get_properties(1).equals(properties.iloc[0])


def test_get_first_property_from_obsdate(sunspotter, obsdate, properties):
    properties.set_index("id_filename", inplace=True)
    assert sunspotter.get_first_property_from_obsdate(
        obsdate).equals(properties.iloc[0])


def test_get_all_properties_from_obsdate(sunspotter, obsdate, properties_csv, timesfits_csv):
    properties_csv.set_index("id_filename", inplace=True)
    idx = timesfits_csv[timesfits_csv.obs_date == obsdate]['#id']
    assert sunspotter.get_all_properties_from_obsdate(
        obsdate).equals(properties_csv.loc[idx])


def test_number_of_observations(sunspotter, obsdate):
    assert sunspotter.number_of_observations(obsdate) == 5


@pytest.mark.parametrize("obsdate,closest_date",
                         [('2000-01-02 00:49:02', '2000-01-02 12:51:02'),
                          ('2000-01-02 00:49:01', '2000-01-01 12:47:02'),
                          ('1999-01-01 00:00:00', '2000-01-01 12:47:02'),
                          ('2100-01-01 00:00:00', '2005-12-31 12:48:02')])
def test_get_nearest_observation(sunspotter, obsdate, closest_date):
    with pytest.warns(SunpyUserWarning):
        assert sunspotter.get_nearest_observation(obsdate) == closest_date


def test_get_all_observations_ids_in_range(sunspotter):
    start = '2000-01-02 12:51:02'
    end = '2000-01-03 12:51:02'
    assert all(sunspotter.get_all_observations_ids_in_range(
        start, end) == np.array([6, 7, 8, 9, 10, 11, 12, 13]))


@pytest.mark.parametrize("start,end,filenames",
                         [('2000-01-02 12:51:02', '2000-01-03 12:51:02',
                           np.array(['20000102_1251_mdiB_1_8810.fits', '20000102_1251_mdiB_1_8813.fits',
                                     '20000102_1251_mdiB_1_8814.fits', '20000102_1251_mdiB_1_8815.fits',
                                     '20000103_1251_mdiB_1_8810.fits', '20000103_1251_mdiB_1_8813.fits',
                                     '20000103_1251_mdiB_1_8814.fits', '20000103_1251_mdiB_1_8815.fits'], dtype=object)),
                          ('2000-01-02 12:51:02', '2000-01-02 12:51:02',
                           np.array(['20000102_1251_mdiB_1_8810.fits', '20000102_1251_mdiB_1_8813.fits',
                                     '20000102_1251_mdiB_1_8814.fits', '20000102_1251_mdiB_1_8815.fits'], dtype=object))])
def test_get_fits_filenames_from_range(sunspotter, start, end, filenames):
    assert all(sunspotter.get_fits_filenames_from_range(
        start, end).values == filenames)


@pytest.mark.parametrize("start,end,obslist",
                         [('2000-01-01 12:47:02', '2000-01-15 12:47:02',
                           pd.DatetimeIndex(['2000-01-01 12:47:02', '2000-01-02 12:51:02',
                                             '2000-01-03 12:51:02', '2000-01-04 12:51:02',
                                             '2000-01-05 12:51:02', '2000-01-06 12:51:02',
                                             '2000-01-11 12:51:02', '2000-01-12 12:51:02',
                                             '2000-01-13 12:51:02', '2000-01-14 12:47:02',
                                             '2000-01-15 12:47:02'],
                                            dtype='datetime64[ns]', name='obs_date', freq=None))])
def test_get_available_obsdatetime_range(sunspotter, start, end, obslist):
    assert all(sunspotter.get_available_obsdatetime_range(
        start, end) == obslist)


def test_rotate_to_midnight(sunspotter, obsdate):
    data = [(Angle(36.97694919 * u.deg), Latitude(24.37393479 * u.deg)),
            (Angle(17.19347675 * u.deg), Latitude(36.4502797 * u.deg)),
            (Angle(61.2536554 * u.deg), Latitude(-28.26438437 * u.deg)),
            (Angle(-21.9812322 * u.deg), Latitude(-16.47798634 * u.deg)),
            (Angle(-43.1676592 * u.deg), Latitude(10.3648738 * u.deg))]

    for index, (lon, lat) in enumerate(sunspotter.rotate_to_midnight(obsdate)):
        assert pytest.approx(lon.value) == data[index][0].value
        assert pytest.approx(lat.value) == data[index][1].value


def test_rotate_list_to_midnight(sunspotter):
    obslist = ['2000-01-02 12:51:02', '2000-01-14 12:47:02']
    data = {
        '2000-01-02 12:51:02': [(Angle(29.18769332 * u.deg), Latitude(36.52576413 * u.deg)),
                                (Angle(-7.76906673 * u.deg),
                                 Latitude(-16.37770425 * u. deg)),
                                (Angle(-22.24109406 * u.deg),
                                 Latitude(10.87542475 * u.deg)),
                                (Angle(-35.77644712 * u.deg), Latitude(10.21004421 * u.deg))],
        '2000-01-14 12:47:02': [(Angle(34.29683246 * u.deg), Latitude(-17.47160603 * u.deg)),
                                (Angle(22.69921514 * u.deg),
                                 Latitude(27.17957675 * u.deg)),
                                (Angle(11.30137214 * u.deg),
                                 Latitude(-32.62222324 * u.deg)),
                                (Angle(-5.21988476 * u.deg),
                                 Latitude(11.55917 * u.deg)),
                                (Angle(63.83616486 * u.deg),
                                 Latitude(17.50447034 * u.deg)),
                                (Angle(60.67931868 * u.deg),
                                 Latitude(-12.83001216 * u.deg)),
                                (Angle(-38.76920932 * u.deg),
                                 Latitude(15.44152655 * u.deg)),
                                (Angle(-54.48209673 * u.deg),
                                 Latitude(-18.30832087 * u.deg)),
                                (Angle(-66.3248029 * u.deg),
                                 Latitude(18.90391944 * u.deg)),
                                (Angle(-10.24376936 * u.deg),
                                 Latitude(-14.82469254 * u.deg)),
                                (Angle(14.22674259 * u.deg), Latitude(-14.43274934 * u.deg))]}

    rotated_dict = sunspotter.rotate_list_to_midnight(obslist)
    for obsdate in rotated_dict:
        for index, (lon, lat) in enumerate(rotated_dict[obsdate]):
            assert pytest.approx(lon.value) == data[obsdate][index][0].value
            assert pytest.approx(lat.value) == data[obsdate][index][1].value


def test_hpc_to_hgs_position(sunspotter, obsdate):
    assert sunspotter.hpc_to_hgs_position(
        obsdate).name == 'heliographic_stonyhurst'


def test_get_lat_lon_in_hgs(sunspotter, obsdate):
    assert isinstance(sunspotter.get_lat_lon_in_hgs(obsdate)[0], Longitude)
    assert isinstance(sunspotter.get_lat_lon_in_hgs(obsdate)[1], Latitude)


def test_match_with_swpc_for_obsdate_default(sunspotter, comparision_df):
    obsdate = '2005-12-31 12:48:02'
    match_result = sunspotter.match_with_swpc_for_obsdate(obsdate)

    for column in comparision_df.columns:
        assert all(np.isclose(match_result[column], comparision_df[column]))


def test_match_with_swpc_for_obsdate_threshold_warning(sunspotter, comparision_df):
    obsdate = '2005-12-31 12:48:02'

    with pytest.warns(SunpyUserWarning):
        match_result = sunspotter.match_with_swpc_for_obsdate(
            obsdate, match_threshold=0)

    for column in comparision_df.columns:
        assert all(np.isclose(match_result[column], comparision_df[column]))
