# Sunspotter - All-Clear dataset

doi: 10.5281/zenodo.1478966

First results based in the All-Clear workshop dataset [1] used on the
zooniverse's [Sunspotter project](https://www.sunspotter.org/).

Volunteers had to choose the most complex active region of a pair based on a
random selection of the least classified images within each binned group.

The dataset is composed of four files:
 - lookup_timesfits.csv: lists the filenames and the date of the data acquisition.
 - lookup_properties.csv: lists the properties about the active region observed
   in each frame to be classified. Some of the properties as measured by SMART [2]
 - classifications.csv: lists each classification made by the volunteers.
 - rankings.csv: lists the final ranking on complexity.

The score provided on the rankings file follows the [Elo rating
system](https://en.wikipedia.org/wiki/Elo_rating_system). However, a new score
following other selection mechanism is possible using the data available on the
classification file.

Though the user's information has been removed, the classifications keep an
index to differentiate classifications made by different users.

Some software to ingest the tables into a sqlite database and to obtain some
preliminary results are available on [GitHub](https://github.com/sunspotter/).

[1]: DOI: [10.3847/0004-637X/829/2/89](https://doi.org/10.3847/0004-637X/829/2/89)

[2]: DOI: [10.1016/j.asr.2010.06.024](https://doi.org/10.1016/j.asr.2010.06.024)



## Header information


### lookup_timesfits.csv

| header   | description                                                |
| ---      | ---                                                        |
| id       | unique identifier for each fits file used on other tables. |
| filename | name of the original fits file used.                       |
| obs_date | date and time of when the image was observed.              |


### lookup_properties.csv

| header        | description                                                                                         |
| ---           | ---                                                                                                 |
| id            | unique identifier for each frame                                                                    |
| filename      | filename of the frame. Prepend http://www.sunspotter.org/subjects/standard/ to see the image.       |
| zooniverse_id | internal zooniverse identifier                                                                      |
| angle         | SMART detection property.                                                                           |
| area          | SMART detection property.                                                                           |
| areafrac      | SMART detection property.                                                                           |
| areathesh     | SMART detection property.                                                                           |
| bipolesep     | SMART detection property.                                                                           |
| c1flr24hr     | at least one C1.0 or greater flare within 24 hr after the observation.                              |
| id_filename   | link to id on lookup_timesfits.csv.                                                                 |
| flux          | SMART detection property.                                                                           |
| fluxfrac      | SMART detection property.                                                                           |
| hale          | Hale (or Mt Wilson) sunspot classification (see http://sidc.oma.be/educational/classification.php). |
| hcpos_x       | heliocentric longitude of the active region's centre.                                               |
| hcpos_y       | heliocentric latitude of the of the active region's centre.                                         |
| m1flr12hr     | at least one M1.0 or greater flare within 12 hr after the observation.                              |
| m5flr12hr     | at least one M5.0 or greater flare within 12 hr after the observation.                              |
| n_nar         | SMART detection property.                                                                           |
| noaa          | NOAA active region number (see https://www.swpc.noaa.gov/products/solar-region-summary).            |
| pxpos_x       | pixel position of the active region's centre along the horizontal axis.                             |
| pxpos_y       | pixel position of the active region's centre along the vertical axis.                               |
| sszn          | sunspotter (formerly sunspotzoo) number. Must be equal to id.                                       |
| zurich        | Zurich sunspot classification (see http://sidc.oma.be/educational/classification.php).              |


### classifications.csv

| header                     | description                                |
| ---                        | ---                                        |
| id                         | unique identifier for each classification. |
| zooniverse_class           | internal identifier.                       |
| user_id                    | user that performed the classification.    |
| image_id_0                 | image identifier from lookup_properties.   |
| image_id_1                 | image identifier from lookup properties.   |
| image0_more_complex_image1 | image number of the complex one.           |
| used_inverted              | whether the user inverted the colours.     |
| bin                        | bin group to where it belongs.             |
| date_created               | dates when the classification happened.    |
| date_started               | dates when the classification happened.    |
| date_finished              | dates when the classification happened.    |


### rankings.csv

| header   | description                                 |
| ---      | ---                                         |
| id       | unique identifier for each ranking.         |
| image_id | image identifier from lookup_properties.    |
| count    | number of classifications of that image.    |
| k_value  | K-factor used for the Elo rating system.    |
| score    | final score based on the Elo rating system. |
| std_dev  | standard deviation.                         |

