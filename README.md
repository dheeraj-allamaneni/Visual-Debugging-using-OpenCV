# Visual Debugging of code using OpenCV

<img src="/images/board_digitalLogic_circuits.png" width="400" />

This board is used in "Digital Logic class" taught here at Iowa State University by Alexander Styotchev and this board is used in that class to design digital circuits.

<img src="/images/2wgbf9.gif" width="400" />\
looks cool right!, but lets just guess whats running in that board.

<img src="https://media.giphy.com/media/yugSj8GSC0wXm/giphy.gif" width="200" />\

### Okay let me give a clear picture of this project

So in the video program runs Bubble sort
* The First four seven segment displays are linked to the first four bytes of the memory
* The last four seven segment displays the registers of the CPU (A, B C and D).

* These papers between led's here are very important(they are dividers between these led's).

* The first six led's show the program counter(where the processor is currently in the memory)
* Next Four LEDs are not used
* Next four led's are the operation call that it is going to perform so essentially that's limited to 16.
* Next 2 led's - set of two bits: for the first register this operation is going to be performed(the previous 4 led's operation) and there are two more(Next two led's)
* These two led's (Led's 21 and 22 between two paper strips) they are the flag register of the ALU: the first one is the negative flag(if the last operation results in a negative number ) and the second one is Zero flag (if you got zero in the last operation).
* Then last two led's are called code fetch and execute cycles, so if the last led is green then it fetches a command and if the last second led is green then it executes.

## Idea behind the project

The idea of this project came in the process of debugging this, it was actually quite a lot fun to debug and the only way to debug is to go back to 1950s when they actually used light bulbs to look through different parts of the process.

 So in this project, we are going back to the 1950s and we are going to have to do a visual disassembly of the program.

## Also i dont want to use any prebuilt OCR libraries or Funtions to detect, but i want to do it from the basic erosion and dilation stuff.

#### Quick fact: The first digital computer "Atanasoff-Berry Computer" - 1942 was built here at Iowa State University and i had chance to see that great machine recently.

<img src="/images/Atanasoff-Berry_Computer_at_Durhum_Center.jpg" width="400" />\

## Part one
### In this part i have detected the numbers on the seven segment display and then Witten text displaying text showing what i have detected above them.

<p float="left">
  <img src="/images/2wqs2u.gif" width="400" />
  <img src="/images/2wqs08.gif" width="400" />
</p>

## Part Two
### In this part i have detected which LED is glowing and where , then displayed their value above them.
<p float="left">
  <img src="/images/2wrg8e.gif" width="400" />
  <img src="/images/2wrgpr.gif" width="400" />
</p>

## Part Three
### In this part i have combined both Part 1 and Part 2 
### Wait!, why dont we do something more - cool - better ?
<img src="https://media.giphy.com/media/SfYTJuxdAbsVW/giphy.gif" width="300" />

#### No, without this the project doesnt feel complete; So the idea is that lets log the Important readings into a text file that help us analyze/debug the Bubble sort program that the machine is Running.

<img src="https://media.giphy.com/media/l4FGjY2RPEjOu5NNC/source.gif" width="300" />

So our program must also output a text file that contains one line for each change of the state of the rightmost green LED (from On to Off or vice versa). The format of the text file should be as follows: 6-bit binary number (the first 6 red LEDs), TAB, an 8-bit binary number (the last 8 red LEDs), TAB, a 2-bit binary number (green LEDs 3 and 4 from left to right), TAB, 2-bit binary number (the last two green LEDs), new line. 

### I have implimented this in part 3 code, and i was able to generate the log, please refer p2c_output.txt

## Final Output
<img src="/images/2wl9n5.gif" width="400" />

Sample text output file:

```text
000000	01100000	00	01	0000	0000

000000	01100000	00	01	0000	0000

000000	01100000	00	11	0000	0000

000000	01100000	00	10	7654	0000

000001	10001100	01	01	7654	0000

000001	10001100	01	01	7654	0000

000001	10001100	01	10	7654	0000

000001	10001100	01	10	7654	0000

000010	01100101	01	01	7654	0003

000010	01100101	01	10	7654	0003

000010	01100101	01	10	7654	0003

000011	01110011	01	01	7654	0003

000011	01110011	01	01	7654	0003

000011	01110011	01	10	7654	0003

000100	11100000	10	01	7654	0003
```
