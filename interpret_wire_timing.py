import json 
import re

# finds the timing info for the given wire 
# also throws an error if we ever break our theory. 
# takes json data and wire as input
def findWireTiming(data, wire ):
    print("Finding wire: " + wire)

def checkAllInstances(wire, pipList, val):
    for pip in dict(pipList): # dict pipList copies the dictionary over so the dictionary size doesn't change while looping
        if re.match("(.*)" + wire, pip):
            print("checking " + pip + ":")
            assert val == (pipList[pip])["src_to_dst"], (pipList[pip])["src_to_dst"]
            del pipList[pip]
    # return pipList

           

# Takes wire name as input. Checks that every instance of ->>WireName has the exact same timing info.
def checkTheory(pipsList):
    with open('/home/chem3000/Programs/prjxray/database/artix7/tile_type_INT_R.json', 'r') as INT_R:
        secondary = json.load(INT_R)

    while len(pipsList) > 0:
        key = next(iter(pipsList))
        if re.match("(.*)(->>)(WW\d+|NN\d+|SS\d+|EE\d+|SW\d+|SE\d+|NW\d+|NE\d+)|(S|N|W|E)(L1|R1)(.*)", key):
            value = pipsList[key]["src_to_dst"] # scopes in python are not in loops or if, only in functions
            wire = key.split("->>")[1]
            checkAllInstances(wire, pipsList, value)
            checkAllInstances(wire, secondary["pips"], value)
            print("\n\n")

            # stop = input("Continue? ")
            # if stop == "n" or stop == "no":
            #     break
        
        else:
            pipsList.pop(key)
        # delete values as you work. 
        # 1) go to the first pip
        # 2) get that pips timing info and delete the pip
        # 3) search through all the pips and check the timing data against the first pip and delete each found pip as you go.
        # 4) if you find a pip that does not comply throw an error and print the pip. 
        # 5) repeat starting at step 1




def main():
    print("Checking INT_L")
    # your json object will be stored as a dictionary where the objects are keys (i.e. pips) and the values are lists. 
    # you will probably have to iterate through the keys and then through the lists.  

    with open('/home/chem3000/Programs/prjxray/database/artix7/tile_type_INT_L.json', 'r') as INT_L:
        data = json.load(INT_L)
        checkTheory(data["pips"])

    # alright here we go this is how things are set up:
    # the entire json file is an object. 
    # pips are a list of json objects.

if __name__ == "__main__":
    main()

# confirmed within the same tile all buffers to a given wire have the same timing info
# confirmed that both INT_L/R have same timing
# the end timing is still an abnormity


# for the anomilies just capture them for the larger blocks since that is what they are for anyway 
# i.e. if you are connecting a L1 to an L1 through a dsp add the proper small timing value. 

# Try to create a timing model. It will be incredibly messy, but it might start getting us in a direction. 



# You will also have to acount for the fact that a lot of the timing for the CB will actually be in xilinx SB. 
# You might be able to take an average of the out wires and get a pretty good approximation.
# 
# I think that https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=8565010&casa_token=pZFOnycMRY0AAAAA:6B96hUdzMu4kTS7zdtQoGk_KKvbB1XPwLCCVDWv_TgD7iwdQtzXBZpOSgo9T6MbMlgdNXOcStg&tag=1
# is actualy worse than symbiflow at least in worst case (20% vs 15% for symbiflow). Might still be worth looking into though.  