# Color Chart Difference Measurement

## Description
   Measure CIELAB chroma difference and CIELAB color difference by color chart.  
  
## Getting Started

### Run the Demo through Executable File
- UNZIP demo.zip and execute "demo.exe"
- In step 1, click "open" button. Select and open the color chart image to be tested.  
- In step 1, click to select the four corner points of the color chart area on the displayed image. Then click "confirm" button.
- In step 2, the cropped color chart area will be displayed. If it does not correspond to the position of the standard color block , click "Rotate 90" button to adjust it to be consistent with the standard color chart.
- In step 3, after the color blocks are aligned, click "Calculate" button to calculate the indicators. Then results are displayed on the right.

### Note
- Button "reset": reset the selected corner points in the image.
- "block scale"：indicates the area of each color block used for calculation. After setting, you need to click "ok" button. The value should be (0,1].
- For standard color chart, please refer to the display interface.

### Run the Demo through Python Code

#### Install Requriements
- python 3.7
- PyQt5
- opencv-python
- numpy
- scipy

#### Run

	python main.py


# Underwater Image Enhancement Method

## UDCP
[Paper](https://ieeexplore.ieee.org/abstract/document/7426236) & [Code](https://github.com/bilityniu/underwater_dark_chennel)
