package riya.bhardwaj;

import android.content.Context;

import com.opencsv.CSVReader;

import androidx.test.InstrumentationRegistry;
import androidx.test.rule.ActivityTestRule;
import androidx.test.runner.AndroidJUnit4;

import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.io.UnsupportedEncodingException;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import androidx.appcompat.app.AppCompatActivity;

import android.content.ContextWrapper;
import android.content.res.AssetManager;
import android.os.Bundle;
/**
 * Instrumented test, which will execute on an Android device.
 *
 * @see <a href="http://d.android.com/tools/testing">Testing documentation</a>
 */
@RunWith(AndroidJUnit4.class)
public class custtableauto{

    //List<Sample>l=new ArrayList<>();
    @Rule
    public ActivityTestRule<RegisterActivity> mActivityRule =
            new ActivityTestRule<>(RegisterActivity.class);
    @Test
    public void automate()  {


        List<Sample> l=new ArrayList<>();

        InputStream is=InstrumentationRegistry.getContext().getResources().openRawResource(R.raw.test);
        BufferedReader reader=new BufferedReader(new InputStreamReader(is, Charset.forName("UTF-8")));
        String line="";
        try{
            while((line=reader.readLine())!=null)
            {
                //Split by ,'s
                String[] tokens=line.split(",");

                //Read the data
                Sample ss=new Sample();
                ss.setFn(tokens[0]);
                ss.setLn(tokens[1]);
                ss.setAdd(tokens[2]);
                ss.setCity(tokens[3]);
                ss.setCoun(tokens[4]);
                ss.setState(tokens[5]);
                ss.setZip(tokens[6]);
                ss.setPh(tokens[7]);
                ss.setEmail(tokens[8]);
                l.add(ss);
            }
            System.out.println(l.get(0).getFn()+" "+l.get(0).getAdd());


        }
        catch(Exception e){
            System.out.println("ohhh");
        }


        /*
        AssetManager assetManager= InstrumentationRegistry.getContext().getAssets();

        try {
            InputStream stream=assetManager.open("C:\\hungry_mind\\app\\src\\main\\assets\\test.csv");
            int size = stream.available();
            byte[] buffer = new byte[size];
            stream.read(buffer);
            stream.close();
            System.out.println(new String(buffer));
        } catch (IOException e) {
            e.printStackTrace();
        }
        */
        /*Scanner scanner = null;
        try {
            scanner = new Scanner(new File("test.csv"));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        ArrayList<String> pokemon = new ArrayList<>();
        while(scanner.hasNextLine()) {
            pokemon.add(scanner.nextLine().split(",")[1]);
        }
        scanner.close();
        */
    }
}
