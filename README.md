# Visual Debugging of code using OpenCV

<img src="/images/board_digitalLogic_circuits.png" width="400" />

This board is used in "Digital Logic class" taught here at Iowa State University by Alexander Styotchev and this board is used in that class to design digital circuits.

<img src="/images/2wgbf9.gif" width="400" />\
looks cool right!, but lets just guess whats running in that board.

<img src="https://media.giphy.com/media/yugSj8GSC0wXm/giphy.gif" width="200" />\

### Okay let me give a clear picture of this project

So in the video program runs Bubble sort
* The First four seven segment displays are linked to the first four bytes of the memory
* The last four seven segemnt displays the registers of the CPU (A, B C and D).

* These papers between led's here are very important(they are dividers between these led's).

* The first six led's show the program counter(where the processor is currently in the memory)
* Next Four leds are not used
* Next four led's are the operation call that it is going to perform so essentially that's limited to 16.
* Next 2 led's - set of two bits : for the first register this operation is going to be performed(the previous 4 led's operation) and there are two more(Next two led's)
* These two led's (Led's 21 and 22 between two paper strips) they are the flag register of the ALU : the first one is the neagative flag(if the last operation results in negative number ) and the second one is Zero flag (if you got zero in last operation).
* Then last two led's are called code fetch and execute cycles, so if the last led is green then it fetches a command and if the last second led is green then it executes.

## Idea behind the project

The idea of this project came in the process of debugging this, it was acutally quite a lot fun to debug and the only way to debug is go back to 1950's when they actually used light bulbs to look through different parts of the process.

 So in this project we are going back to 1950's and we are going to have to do a visual disassembly of the program.
 
#### Quick fact: The first digital computer "Atanasoff-Berry Computer" - 1942 was built here at Iowa State University and i had chance to see that great machine recently.
<img src="/images/Atanasoff-Berry_Computer_at_Durhum_Center.jpg" width="400" />\
