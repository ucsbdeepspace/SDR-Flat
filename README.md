Sahil S. Mahajan
sahilgotsoul@gmail.com
(909) 260 8562

Once downloaded, run:
mkdir build
cd build
cmake ../
make
sudo make install
sudo ldconfig

Be sure to place "gr-sahil" and "airspy_spectrum_analyzer.py" into the root directory of GNURadio

The best way to modify airspy_spectrum_analyzer.py is to open GRC and open airspy.grc. Make changes in the flow diagram and push the "Generate" button. Pushing this button updates the code.

airspy_spectrum_analyzer.py depends on the files in gr-sahil. These files are save_N_to_h5.py, average.py, and addheaders.py

save_N_to_h5 saves N items to an h5 file before starting a new h5 file.

average performs a block average for each time interval. This block does not work, and should be either modified or removed from the block diagram airspy.grc. One reason this does not work is because it is a "sync" type block, while its work function performs an average for a number of spectra, thus decimating the stream. Consider making a "general" type block with a similar code. When changing this block, keep in mind that some of the input stream might have a first dimension of greater than 1.
Once this is changed, write your name and run the above commands to install.


addheaders adds to each spectrum the timestamp, the starting frequency, the bandwidth, and the number of bins. This block calculates the timestamp for each spectrum from the 10 MSPS of the airspy and the decimation factors of the FFT block.


There is one problem with this code so far. If you connect this block to the save_N_to_h5 block, and disable the average block, the code returns an error and says to consider using a power-of-two number. This might be due to the addheaders block, which adds 4 new elements to each spectrum as headers. A possible way to solve this problem is to use stream tags instead of the addheaders block.
