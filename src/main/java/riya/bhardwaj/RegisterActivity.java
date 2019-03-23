package riya.bhardwaj;

import androidx.appcompat.app.AppCompatActivity;

import com.amazonaws.auth.AWSCredentialsProvider;
import com.amazonaws.mobile.client.AWSMobileClient;
import com.amazonaws.mobile.config.AWSConfiguration;
import com.amazonaws.mobileconnectors.dynamodbv2.dynamodbmapper.DynamoDBMapper;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClient;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.List;

public class RegisterActivity extends AppCompatActivity {

    //List<Sample> l=new ArrayList<>();
    DynamoDBMapper dynamoDBMapper;
    EditText name,password,phone,email,address;
    Button submit;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        // AWSMobileClient enables AWS user credentials to access your table
        AWSMobileClient.getInstance().initialize(this).execute();
        AWSCredentialsProvider credentialsProvider = AWSMobileClient.getInstance().getCredentialsProvider();
        AWSConfiguration configuration = AWSMobileClient.getInstance().getConfiguration();


        // Add code to instantiate a AmazonDynamoDBClient
        AmazonDynamoDBClient dynamoDBClient = new AmazonDynamoDBClient(credentialsProvider);

        this.dynamoDBMapper = DynamoDBMapper.builder()
                .dynamoDBClient(dynamoDBClient)
                .awsConfiguration(configuration)
                .build();
/*
        InputStream is=getResources().openRawResource(R.raw.us);
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
*/

        System.out.println("executed properly");
        name=(EditText)findViewById(R.id.name);
        password=(EditText)findViewById(R.id.pass1);
        phone=(EditText)findViewById(R.id.phone1);
        submit=(Button)findViewById(R.id.submit);
        email=(EditText)findViewById(R.id.email);
        address=(EditText)findViewById(R.id.address);
        submit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                createItem();
            }
        });

    }
    public void createItem() {
        final CustomerTableDO Item = new CustomerTableDO();
        int id=1000;
       // for(int i=0;i<500;i++) {
            String n = name.getText().toString();
            String e = email.getText().toString();
            String p = password.getText().toString();
            String a = address.getText().toString();
            double num = (Double.parseDouble(phone.getText().toString()));

            /*String n=l.get(i).getFn()+l.get(i).getLn();
            String e=l.get(i).getEmail();
            String p=l.get(i).getState()+l.get(i).getZip();
            String a=l.get(i).getCity()+","+l.get(i).getCoun()+","+l.get(i).getState();
            String inp=l.get(i).getPh();
            String ff="";
            for(int j=0;j<inp.length();j++)
            {
                if(inp.charAt(j)!='-')
                    ff+=inp.charAt(j);
            }
             double num=Double.parseDouble(ff);
             */
            Item.setCustName(n);
            Item.setCustEmail(e);
            Item.setCustNumber(num);
            Item.setCustPassword(p);
            Item.setCustAddress(a);
            Item.setCustId((double) 2040);
            id+=1;

            new Thread(new Runnable() {
                @Override
                public void run() {
                    dynamoDBMapper.save(Item);
                    // Item saved
                }
            }).start();
        //}
    }
}
