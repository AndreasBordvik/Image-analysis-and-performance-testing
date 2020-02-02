Note to the report.txt files:
Runtime depends on many factors. The runtime speed is not run with proper statistical analysis. 


### 4.1 - Python implementation:
How to run blur_1.py with parameters:
It is only required to specify the input file name. But the script 
can take upto 3 arguments. 
`1: The input file. `
`2: The output filename with or without a filepath`
`3: Number of blur cycles (int value of 1 to 999999. Default value is 1) `
Examples:
python3 blur_1.py beatles.jpg
python3 blur_1.py beatles.jpg python_blur.jpg
python3 blur_1.py beatles.jpg python_blur.jpg 2


### 4.2 - Numpy implementation:
How to run blur_2.py with parameters:
It is only required to specify the input file name. But the script 
can take upto 3 arguments. 
`1: The input file. `
`2: The output filename with or without a filepath`
`3: Number of blur cycles (int value of 1 to 999999. Default value is 1) `
Examples:
python3 blur_2.py beatles.jpg
python3 blur_2.py beatles.jpg numpy_blur.jpg
python3 blur_2.py beatles.jpg numpy_blur.jpg 4


### 4.3 - Numba implementation:
How to run blur_3.py with parameters:
It is only required to specify the input file name. But the script 
can take upto 4 arguments. 
`1: the input file. `
`2: The output filename with or without a filepath`
`3: number of blur cycles (int value of 1 to 999999. Default value is 1) `
`4: vectorized algorithm or none vectorized (True = vectorized)`
Nonvectorized is the default algorithm that the numba implementation will use. 
True on the forth argument will run the vectorized algorithm.
Examples:
python3 blur_3.py beatles.jpg
python3 blur_3.py beatles.jpg numbaVec.jpg
python3 blur_3.py beatles.jpg numbaVec.jpg 4
python3 blur_3.py beatles.jpg numbaVec.jpg 4 True


### 4.4 - Cython implementation:
How to run blur_4.py with parameters:
It is only required to specify the input file name. But the script 
can take upto 4 arguments. 
`1: The input file. `
`2: The output filename with or without a filepath`
`3: Number of blur cycles (int value of 1 to 999999. Default value is 1) `
`4: Vectorized algorithm or none vectorized (True = vectorized)`
Nonvectorized is the default algorithm that the Cython implementation will use. 
True on the forth argument will run the vectorized algorithm.
Examples:
python3 blur_4.py beatles.jpg
python3 blur_4.py beatles.jpg cythonUnVec.jpg
python3 blur_4.py beatles.jpg cythonUnVec.jpg 4
python3 blur_4.py beatles.jpg cythonVec.jpg 4 True


### 4.5 User interface:
The assignment text states that we shall make a script. I have made the script 
so that it only calls a main method/function. The main function contains all the user 
interface code. The main function is only "automatically" called if blur.py file 
is run directly from the assignment folder. 
From the installed package, blur can be imported like this:
"from imageblurring.blur import main as blur".
I have made it like this to prevent the script from running if you only import using
"import imageblurring.blur". Import like this would always have excecuted the script automatically 
just from the import line itself. To prevent scripts from executing direclty from the import line,
the code is moved into a function that must be called. blur.py must either run direcly from the folder, 
or must be imported from a installed package using "from imageblurring.blur import main as blur" 
followed by a function call on blur(). Argparse is passed into the main method inside blur.py, 
and the main method is than executed.
 
Some lines are abit long in flake8, but they are kept a few chars to long to 
maintain readability. The blur_image function is located in the imagefunctions.py file.


### 4.6 Packaging and unit tests:
Unit testing:
Is performed using pytest test_blur.py from the test folder.

Package guide:
Installing the package:
In the assignment4 folder where the setup.py file is located run:
python3 -m pip install -r requirements.txt
python3 -m pip install .


Using the package after installation (two choises):
`1)`
`Move the folder assignment4/tests/PackageTest into aa different directory than assignment4.`
`Run packageTestBlur.py and packageTest.py`

`2)`
`Create a new python file and give it a name in a different folder than `
`assignment4 directory or subdir. `
`Place the picture called beatles.jpg in this folder created together with the`
`xml file called haarcascade_frontalface_default.xml.`

Code example on how to test the package after installation:
from imageblurring.blur import main as blur
from imageblurring.blur_1 import main as blur1
from imageblurring.blur_2 import main as blur2
from imageblurring.blur_3 import main as blur3
from imageblurring.blur_4 import main as blur4
from imageblurring.blur_faces import main as bf
from imageblurring.imagefunctions import blur_image

inFile = "beatles.jpg"
cascadeFile="haarcascade_frontalface_default.xml"
blur1(inFile, "blur1_test_image.jpg", 1)
blur2(inFile, "blur2_test_image.jpg", 15)
blur3(inFile, "blur3_test_image.jpg", 20, False)
blur4(inFile, "blur4_test_image.jpg", 20, False)
blur_image(inFile, "blur_image_test_image.jpg")
bf(inFile, "blur_faces_test_image.jpg", cascadeFile)
blur()

Uninstalling the package:
python3 -m pip uninstall ImageBlur


### 4.7 - Blurring faces:
How to run blur_faces.py with parameters:
`1: The input file. `
`2: The output filename with or without a filepath`
`3: Cascade xml filename with or without a filepath `
Example:
blur_faces("beatles.jpg", "blur_faces_test_image.jpg", "haarcascade_frontalface_default.xml")
