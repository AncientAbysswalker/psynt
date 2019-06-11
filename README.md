# psynt

## Problem Statement
We want to ask questions of a subject, analyse the answers, and provide results based on said answers.

## Solution
Using experience and knowledge from another project where I am developing an application in python, I set out to develop a simple prototype. This prototype uses wxPython to render all the necessary details of the application.

All information provided to me was converted into yaml files and text files, as these were the easiest methods of storing the information I was provided - and I do not have a need to set up a full and proper database. 

As this was developed per a request, I have changed the actual content of the questions and answer-to-result conversion database to not contain minimal amounts of the original information. I've included some slightly unnecessary segmentation such as the config.py file so that I can have one set of information for the repo online to show my work, and a separate one for production.

This application example takes your answers and converts them into recommended colors, including links to a site where you can observe said colors. The production copy of the application functions in a similar manner.