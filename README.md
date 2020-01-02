# coffeeMisc

Firstly I must say this project would not be possible without the incredible program written by J Gagne at https://coffeeadastra.com.
Many parts have been taken directly from his source code which can be found at:
https://github.com/jgagneastro/coffeegrindsize

My code here takes data collected by his coffee grind size app, stored in .csv files, and puts it into a readable form for multiple grind settings. 
Statistics is not something I'm incredibly familiar with, so if I have misrepresented any data here please let me know.


This is a project I undertook at our coffee lab to quantify if the tastes we experienced on our Mahlkonig EK-43, and the visual appearance of ground coffee, were due to misaligned burrs. I was also curious if a fit model could produce a useful description of each grind setting and the change between them.

Upon initial inspection the burrs were misaligned slightly both axially and radially. The burrs were also notably dull, and should likely be changed sometime soon. Another round of tests will follow if that occurs. After shimming and aligning the faceplate-side burrs there was a noticeable improvement in grind passthrough time (less time for residuals to exit the grinding chamber), a seeming improvement in the naked-eye appearance of ground coffee's size uniformity, as well as a qualitative improvement in flavor, especially brew-to-brew at our typical grind setting.

Re-taking data post-alignment shows improvements in both grind quality and grind-setting change linearity. However upon inspection the burrs did appear and feel quite dull and should likely be replaced in the near future. Given the large spread in grind size distribution, it is unlikely the parameters of the linear fit model can adequately describe particle-size in a grinder-to-grinder comparison.

For a full write-up on this topic please see my post at our website: https://flightcoffeeco.com/blogs/news/our-mahlkonig-ek-43s-grind-quality
