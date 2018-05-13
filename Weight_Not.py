#Weight Not, Want Not
#How much does your new smartphone really weigh?
#https://twitter.com/weight_not_want
#(Short essay at the bottom)

import pandas as pd
import tweepy
import numpy as np
import random
import math
from PIL import Image

#Copyright 2018 Adriaan Odendaal
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

consumerKey = 'hM1xXDUk2AfA7HsOaAxXlzM7w'
consumerSecret = 'bj2GthZmyyeUZQSA7XnNELaJLY9JseVPycdgCIxM6PJ1ckfwZc'
accessToken = '987576114011885570-ySAnYNTC2HdJAKAlYYuqg8AIgFFnAlB'
accessTokenSecret = '4YL52tUrdVfBvwRqNJ1TmNN85RK0ZOcXIa2kJ7gwLohBG'
#logins: ad.riaan.odendaal1@gmail.com wadriaan28

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

def main ():
  partOne, partTwo = compiler()
  tweetText(partOne,partTwo)
  
def compiler():
  company = selecterPhone()
  partOne, weightWeek = thisWeekPhone(company)
  numberThings,things, thingImage = equavalentTo(weightWeek)
  if things[-1] == 's':
    partTwo = numberThings+' '+things+'es'
  else:
    partTwo = numberThings+' '+things+'s'
  imageCompiler(thingImage,numberThings)
  return partOne, partTwo
  
  
def imageCompiler(thingImage,numberThings):
  print '\n','imageCompiler()------', '\n'
  measure = float(numberThings)
  rows = 0
  columns=1
  if measure ==2:
    columns=2
    rows=int(math.ceil(measure/2))
  if measure >2:
    columns=4
    rows=int(math.ceil(measure/4))

  result = Image.new("RGB", ((400*columns), (400*rows)), "white") 
  print 'Image array created: ',columns, 'columns (x)',rows, 'rows (y)','\n','Image dimensions: ' ,result.size
  counter=0
  
  columncounter=0
  print '\n','---Compiling image on blank canvas---','\n'
  for number in range(0,int(measure)):
    print 'Copy number: ', number,'Counter: ',counter,'Column counter',columncounter
    image = Image.open('images/'+thingImage)
    if columncounter==4:
     columncounter=0
     counter=counter+400
    result.paste(image, (400*columncounter,counter))
    columncounter=columncounter+1
     
  print '\n','---Saving image---'
  result.save('image3.jpg')
  

  
def tweetText(partOne,partTwo):
  print '\n','tweetText()------'
  sentenceFull= partOne+ ', roughly equavalent to the weight of '+partTwo
  print '\n','Sentence full: ', sentenceFull
  print '\n','---Publishing Tweet---'
  api.update_with_media('image3.jpg', status=sentenceFull)
   
def equavalentTo(weightWeek):
  #dictionary with all values and their positions in
  print '\n','equavalentTo()------'
  dataFArray=spreadSheetReader('Weight of things')
  listofThings=[]
  thingsTuples =()  
  for number in range(0,len(dataFArray)):
    thingsTuples=(str(dataFArray[number,0]),int(dataFArray[number,1]))
    listofThings.append(thingsTuples)
  print '\n', 'Data array to compare weights to:','\n' ,dataFArray,'\n'

  #Make a list of random objects in list 
  print '---Making comparisons---','\n'
  
  counter =[]
  for number in range (0,3):
    randomNumber = random.randint(0,3)
    while randomNumber in counter:
      	randomNumber = random.randint(0,3)
    counter.append(randomNumber)
  print 'List of random numbers in list:',counter 
  
  remainderTrue = 0
  equalToTrue =0
  countTrue = 0
  for count in counter:
    print 'Random number from list:',count
    number = (float(listofThings[int(count)][1])) #selectes the thing in list's weight and convert from kg to metric ton
    print 'Number:', number
    equalTo= weightWeek/number
    print 'Weight of thing: ', number, ' Weight of phones per week: ',weightWeek, ' Equalto: ', equalTo
    remainder=weightWeek % equalTo
    if count == counter[0]:
      remainderTrue = remainder
      print 'remainderTrue: ',remainderTrue
    print 'There are: ', int(equalTo),' of object', (listofThings[int(count)][0]), 'whose weight is',int(number), 'in', weightWeek ,' with ', remainder, ' remaining'
    print 'remainder:',remainder,'remainderTrue:',remainderTrue
    if remainder <= remainderTrue and remainder>=0:
      remainderTrue=remainder
      equalToTrue=int(equalTo) 
      countTrue=count	  
      print 'TOP:','There are: ', int(equalTo),' of object', (listofThings[int(count)][0]), 'whose weight is',int(number), 'in', weightWeek ,' with ', remainder, ' remaining'
  print '\n','FINAL:','There are: ', equalToTrue,' of object', (listofThings[int(countTrue)][0]),'in', weightWeek ,' with ', remainderTrue ,'remaining'
  return str(equalToTrue), str(listofThings[int(countTrue)][0]), dataFArray[int(countTrue),2]
	
def selecterPhone():
  print 'selecterPhone()------'
  options = ('Apple','Samsung','Huawei')
  fileRead=open('phonecounter.txt', 'r')
  fileList=fileRead.readlines()
  counter=int(fileList[0])
  fileRead.close()
  print 'Counter: ', counter
  fileWrite=open('phonecounter.txt', 'w')  
  if counter==2:
    fileWrite.write('0')
  else:
    fileWrite.write(str(counter+1))
  fileWrite.close()
  
  phoneselected =options[counter]
  print 'Phone Selected: ',phoneselected
  return phoneselected

def spreadSheetReader(sheetName):
  XLRead = pd.ExcelFile('Weights.xlsx')
  dataF = XLRead.parse(sheetName)
  dataFString=dataF.astype(str).values #turn into strings without u' (unicode) https://stackoverflow.com/questions/13187778/convert-pandas-dataframe-to-numpy-array-preserving-index
  dataFArray=np.asarray(dataF)
  return dataFArray
  
def thisWeekPhone(company):
  print '\n','thisWeekPhone()------'
  phones = ''
  dataFArray=spreadSheetReader(company)
  if company == 'Apple':
    phones = '#iPhone devices'
  else:
    phones = '#smartphone devices'
  
  print '\n','---Reading Spreadsheet---','\n'
  phoneWeight = (dataFArray[9,1])
  phonePerWeek = (dataFArray[10,5])*1000000
  weightWeek =int((phonePerWeek*phoneWeight)/1000)
  
  print 'Phones per week: ',int(phonePerWeek),company, ' sold on average per week'
  print 'Weight per week (weightWeek): ',weightWeek,'kg of',phones,' sold on average per week'
  partOne = 'This week we consumed an estimate '+str(weightWeek)+'kg of '+'#'+company+ ' '+phones
  print 'Part one complete: ', partOne
  return partOne, weightWeek

if __name__ == "__main__":
  main()
  
#Waste Not Want Not is a bot that tweets the amount of phones we as consumers collectively buy from the 3 biggest vendors each week (the data is taken from average weekly phone sales for each company over the four quarters of 2017). 
#However, this bot does not tweet in the 'quarterly-report' measure of 'units sold', but rather in terms of how much material mass has been sold (and by extension, produced). 
#This is an effort to show how each of the pristinely designed and packaged single devices that we buy in increasingly quickening cycles contributes to a mass resource consumption. 
#This becomes increasingly pertinent as the rising numbers in the quarterly-reports of the ever-growing tech-behemoths is underlined by a mass-production model founded on planned-obsolescence and a fetishization of 'cutting-edge' technological novelty and upgrade successions.
#The purpose of this bot is to hint (however lightly) at what our digital devices fundamentally are: commodified material goods produced from increasingly limited natural resources. 
