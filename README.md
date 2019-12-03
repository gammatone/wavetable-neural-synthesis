# wavetable-neural-synthesis

## Requirements

### Python3 (Windows)

#### Install *pip*, *virtualenv* packages
```
$ python3 -m pip install --upgrade pip
$ python3 -m pip install --upgrade virtualenv
```
Create a new virtual environment in directory of your choice:
```
$ python3 -m venv ./my_venv_name
```
Activate virtual environment:
```
$ .\my_venv_name\Scripts\activate
```
#### Install/upgrade packages within a virtual environment

*pip*
```
$ python3 -m pip install --upgrade pip
```
*tensorflow*

If you have a **compatible GPU**:
```
$ python3 -m pip install --upgrade tensorflow-gpu
```
See [here](https://www.tensorflow.org/guide/gpu) to test that TensorFlow is using the GPU.

Else:
```
$ python3 -m pip install --upgrade tensorflow
```

When done with virtual environment:
```
$ deactivate
```

## Dataset

Collect waveform data and wrap it into a generic format.

### AKWF dataset (from Git repository)

AKWF or Adventure Kid Waveforms is a collection of one cycle waveforms to be used within synthesizers or other kinds of sound generators.

To clone repository into ````./data/raw_data```` directory:
```
$ cd scripts
$ python3 ./get_akwf_dataset.py
```