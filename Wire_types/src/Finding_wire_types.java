import com.xilinx.rapidwright.design.Design;
import com.xilinx.rapidwright.design.Net;
import com.xilinx.rapidwright.device.Device;
import com.xilinx.rapidwright.device.PIP;
import com.xilinx.rapidwright.tests.CodePerfTracker;

import java.util.HashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import static com.trolltech.qt.gui.QTextOption.WrapMode.WordWrap;

// How to include wrappid wright: file->project structure->modules->Dependencies->+ icon->external libraries-> add jars from rappid write folder
// Get the rapidwright-2022.2.2-standalone-lin64.jar

class MutableInt {
    int value = 0; // note that we start at 1 since we're counting
    MutableInt(){}

    MutableInt(int value){
        this.value = value;
    }
    public void increment () { ++value;      }
    public int  get ()       { return value; }
    @Override
    public String toString(){
        return String.valueOf(value);
    }
}

public class Finding_wire_types {

    // From BING AI
    public static void wrapText(String text, int lineLength) {
        int i = 0;
        while (i < text.length()) {
            int nextSpace = text.indexOf(' ', i + lineLength);
            if (nextSpace == -1) {
                System.out.println(text.substring(i));
                return;
            }
            System.out.println(text.substring(i, nextSpace));
            i = nextSpace + 1;
        }
    }


    public static void main(String args[]){
        Design design = Design.readCheckpoint("/home/chem3000/GitClones/vtr-xilinx-comp/sha.dcp", CodePerfTracker.SILENT);

        System.out.println("The part number for this device is: " + design.getPartName() +"\n");

        Device device = design.getDevice();

        Map wire_counts = new HashMap<String, MutableInt>();

        // Cardinal

        wire_counts.put("WL1", new MutableInt());
        wire_counts.put("WR1", new MutableInt());
        wire_counts.put("WW2", new MutableInt());
        wire_counts.put("WW4", new MutableInt());
        wire_counts.put("WW6", new MutableInt());

        wire_counts.put("EL1", new MutableInt());
        wire_counts.put("ER1", new MutableInt());
        wire_counts.put("EE2", new MutableInt());
        wire_counts.put("EE4", new MutableInt());
        wire_counts.put("EE6", new MutableInt());

        wire_counts.put("NL1", new MutableInt());
        wire_counts.put("NR1", new MutableInt());
        wire_counts.put("NN2", new MutableInt());
        wire_counts.put("NN4", new MutableInt());
        wire_counts.put("NN6", new MutableInt());

        wire_counts.put("SL1", new MutableInt());
        wire_counts.put("SR1", new MutableInt());
        wire_counts.put("SS2", new MutableInt());
        wire_counts.put("SS4", new MutableInt());
        wire_counts.put("SS6", new MutableInt());


        // Inter-cardinal
        wire_counts.put("NW2", new MutableInt());
        wire_counts.put("NW4", new MutableInt());
        wire_counts.put("NW6", new MutableInt());

        wire_counts.put("NE2", new MutableInt());
        wire_counts.put("NE4", new MutableInt());
        wire_counts.put("NE6", new MutableInt());

        wire_counts.put("SW2", new MutableInt());
        wire_counts.put("SW4", new MutableInt());
        wire_counts.put("SW6", new MutableInt());

        wire_counts.put("SE2", new MutableInt());
        wire_counts.put("SE4", new MutableInt());
        wire_counts.put("SE6", new MutableInt());


       for(Net net : design.getNets()){
//            might have to loop through the sites to get from source pin to dst pin.

            for (PIP pip : net.getPIPs()){
                // always look at the wire on the recieving side of the pip
                String wire = pip.getEndWireName();
                Pattern pattern = Pattern.compile("(WL|WR|SL|SR|ER|EL|NL|NR)1|(WW|EE|NN|SS|NE|NW|SE|SW)\\d+");
                // Note there is a zero length wire (i.e. EL0)?
                Matcher matcher = pattern.matcher(wire);
                if(matcher.find()){
                    try {
                        ((MutableInt) wire_counts.get(matcher.group(0))).increment();
//                        System.out.printf("Inc wire: %s\n", wire.toString());
                    } catch (Exception e){
                        System.out.println(e);
                        System.out.println("At value " + matcher.group(0));
                        System.exit(1);
                    }
                }
            }
        }
       String [] len1Names = new String[]{"WL1", "WR1", "WW1", "EL1", "ER1", "EE1", "NL1", "NR1", "NN1", "SL1", "SR1", "SS1"};
       for(int i = 0; i < 4; i++){
           int val1 = ((MutableInt)wire_counts.remove(len1Names[i*3])).get();
           int val2 = ((MutableInt)wire_counts.remove(len1Names[i*3+1])).get();

           wire_counts.put(len1Names[i*3+2], new MutableInt(val1 + val2));

       }

       System.out.printf("WW_EE1: %d\n", ((MutableInt)wire_counts.get("WW1")).get()+((MutableInt)wire_counts.get("EE1")).get());
        System.out.printf("NN_SS1: %d\n", ((MutableInt)wire_counts.get("NN1")).get()+((MutableInt)wire_counts.get("SS1")).get());
        System.out.printf("WW_EE2: %d\n", ((MutableInt)wire_counts.get("WW2")).get()+((MutableInt)wire_counts.get("EE2")).get());
        System.out.printf("NN_SS2: %d\n", ((MutableInt)wire_counts.get("NN2")).get()+((MutableInt)wire_counts.get("SS2")).get());
        System.out.printf("NN_SS4: %d\n", ((MutableInt)wire_counts.get("NN4")).get()+((MutableInt)wire_counts.get("SS4")).get());
        System.out.printf("WW_EE4: %d\n", ((MutableInt)wire_counts.get("WW4")).get()+((MutableInt)wire_counts.get("EE4")).get());
        System.out.printf("WW_EE6: %d\n", ((MutableInt)wire_counts.get("WW6")).get()+((MutableInt)wire_counts.get("EE6")).get());
        System.out.printf("NN_SS6: %d\n", ((MutableInt)wire_counts.get("NN6")).get()+((MutableInt)wire_counts.get("SS6")).get());
        System.out.printf("NE_SW6: %d\n", ((MutableInt)wire_counts.get("NE6")).get()+((MutableInt)wire_counts.get("SW6")).get());
        System.out.printf("NW_SE6: %d\n", ((MutableInt)wire_counts.get("NW6")).get()+((MutableInt)wire_counts.get("SE6")).get());
        System.out.printf("NE_SW2: %d\n", ((MutableInt)wire_counts.get("NE2")).get()+((MutableInt)wire_counts.get("SW2")).get());
        System.out.printf("NW_SE2: %d\n", ((MutableInt)wire_counts.get("NW2")).get()+((MutableInt)wire_counts.get("SE2")).get());






//        for (Object entry : wire_counts.entrySet()) {
//
//        }
    }
}
