Prior Evaluation Tool:

To set up the conda envronment required for the PET use the command:
`conda env create -f environment_PET.yml`

I have included several models for utilising the tool and demonstrating its capabilites:

The height model that was utilized in the dissertation is in the file height_model_example
To run this and create the tool use the command:
'python height_model_example.py'

Some other examples can be run using:
'python mining_disaster_example.py'
'python linear_regression_example.py'


The unit tests can be run using the command:
'python -m unittest discover tests'