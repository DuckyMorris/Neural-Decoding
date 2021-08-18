# Neural-Decoding
Research Project on live time neural decoding to insert into Open Ephys pipeline. Full project includes using the Open Ephys GUI with a ZMQ plugin.

Due to Jupytyer Notebooks, the live updating are not shown in the notebook, so a videos are in the visuals folder.

data.py defines a Data object that contains the spike sorted data from the ratser files, the labels and time stamps. This defines a function bin_data which puts the raster data into bins of a certain length and returns the same data object type.

ExtractMat.py defines function get_mat_data() which reads the matlab files in the folder Zhang_Desimone_7objects_raster_data and the binnded data from ZD_150bins_50sampled.Rda.

helpers.py defines various helper functions used in the different programs.

ml.py contains our machine learning algorithm with a training function, train() which returns our model, and a predicting function, predict, which makes a prediction based on our model earlier.

plots.py contains functions that update our two plots

TransformRaster.py defines a function transform_raster() converts our raw raster data read from the files to a matrix format.

transform_files.py is program that should be run before our simulate_live.py program. It uses many of the functions described above to generate a pseudopopulation and saves the various data by pickling it into files to be used later by our simulate_live.py program.

simulate.live.py is the main program that has a loop that is supposed to mimic live data and makes predictions, trains the model and provides some visuals for the user.

To run the the simulation type, 

```shell
python transform_files.py
```
and then,

```shell
python simulate_live.py
```
in the command prompt.
