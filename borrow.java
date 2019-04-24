package riya.bhardwaj;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Toast;

import com.amazonaws.auth.AWSCredentialsProvider;
import com.amazonaws.mobile.client.AWSMobileClient;
import com.amazonaws.mobile.config.AWSConfiguration;
import com.amazonaws.mobileconnectors.dynamodbv2.dynamodbmapper.DynamoDBMapper;
import com.amazonaws.mobileconnectors.dynamodbv2.dynamodbmapper.DynamoDBScanExpression;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClient;

import java.text.SimpleDateFormat;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.List;
import java.util.Locale;
import java.util.Random;
import java.util.concurrent.ThreadLocalRandom;


public class borrow extends AppCompatActivity {

    DynamoDBMapper dynamoDBMapper;
    public List<CustomerTableDO> list = new ArrayList<>();
    public List<BooksDO> list1 = new ArrayList<>();
    public List<Double> custid = new ArrayList<>();
    public List<Double> bookid = new ArrayList<>();

    public static int randBetween(int start, int end) {
        //int random = (int )(Math.random() * end + start);
        Random r = new Random();
        int result = -1;
        try {
            result = r.nextInt(end - start) + start;
        } catch (Exception e) {
            System.out.println(e);
        }
        //return start + (int)Math.round(Math.random() * (end - start));
        return result;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_borrow);

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


        //DynamoDB dynamoDB = new DynamoDB(client);
        final DynamoDBScanExpression scanExpression = new DynamoDBScanExpression();
        Thread t = new Thread(new Runnable() {
            @Override
            public void run() {

                List<CustomerTableDO> list2 = dynamoDBMapper.scan(CustomerTableDO.class, scanExpression);
                list = list2;

                int i = 0;
                while (i < list.size()) {
                    custid.add(list2.get(i).getUserId());
                    System.out.println(custid.get(i));
                    i += 1;
                }
                System.out.println("customers done " + list.size());

            }
        });
        t.start();
        try {
            t.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        final DynamoDBScanExpression scanExpression2 = new DynamoDBScanExpression();
        Thread t1 = new Thread(new Runnable() {
            @Override
            public void run() {

                List<BooksDO> list2 = dynamoDBMapper.scan(BooksDO.class, scanExpression2);
                list1 = list2;

                int i = 0;
                while (i < list.size()) {
                    custid.add(list2.get(i).getISBN());
                    System.out.println(custid.get(i));
                    i += 1;
                }
                System.out.println("books done " + list1.size());

            }
        });
        t1.start();
        try {
            t1.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

Thread t3=new Thread(new Runnable() {
    @Override
    public void run() {
        //custid,bookid
        int arr[] = new int[24];
        int j = 0;

        for (int i = 7; i <= 30; i++, j++) {
            arr[j] = i;
        }
        //SimpleDateFormat dfDateTime  = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss", Locale.getDefault());
        if (custid.size() > 0 && bookid.size() > 0) {
            ArrayList<Integer>stored=new ArrayList<>();
            System.out.println("start");
            int borrid = 100;
            String suppid = "1";
            List<Sample3> l = new ArrayList<>();
            for (int i = 0; i < 1000; i++) {
                int cus = randBetween(0, custid.size() - 1);
                int boo=0;
                while(stored.contains(boo) )
                {
                    boo = randBetween(0, bookid.size() - 1);

                }
                stored.add(boo);

                System.out.println(cus + " " + boo);

                int month = randBetween(1, 12);

                System.out.println(month);

                int day = 1;
                int day2 = 8;
                int month2 = month, year2;
                int year = randBetween(1900, 2019);

                System.out.println(day + " " + day2 + " " + month2 + " " + year);

                year2 = year;
                int dur = randBetween(0, 23);


                int day3, month3, year3;
                int are[] = {-4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7};
                int durre = randBetween(0, 11);
                System.out.println(year2 + " " + dur);

                if (month == 4 || month == 6 || month == 9 || month == 11) {
                    System.out.println("hey");
                    day = randBetween(1, 30);
                    day2 += arr[dur];

                    if (day2 > 30) {
                        day2 = day2 - 30;
                        month2++;
                    }
                    if (month2 > 12) {
                        month2 = 1;
                        year2++;
                    }
                    System.out.println("hey");

                } else if (month == 2) {
                    System.out.println("hey2");
                    day = randBetween(1, 28);
                    day2 += arr[dur];
                    if (day2 > 28) {
                        day2 = day2 - 28;
                        month2++;
                    }
                    if (month2 > 12) {
                        month2 = 1;
                        year2++;
                    }
                    System.out.println("hey2");
                } else {
                    System.out.println("hey3");
                    day = randBetween(1, 31);
                    day2 += arr[dur];
                    if (day2 > 31) {
                        day2 = day2 - 31;
                        month2++;
                    }
                    if (month2 > 12) {
                        month2 = 1;
                        year2++;
                    }
                    System.out.println("hey3");
                }
                System.out.println("hey4");
                System.out.println(day + "-" + month + "-" + year);
                System.out.println(day2 + "-" + month2 + "-" + year2);

                day3 = day2 + are[durre];
                month3 = month2;
                year3 = year2;
                System.out.println(month3 + "-" + day3 + "-" + year3);
                if (month2 == 1) {
                    if (day3 < 1) {
                        day3 = 31;
                        month3 = 12;
                        year3 = year2 - 1;
                    }
                    if (day3 > 31) {
                        day3 = 1;
                        month3 = 2;
                        year3 = year2 + 1;
                    }
                }
                if (month2 == 2) {
                    if (day3 < 1) {
                        day3 = 31;
                        month3 = 1;
                        year3 = year2;
                    }
                    if (day3 > 28) {
                        day3 = 1;
                        month3 = 3;
                        year3 = year2;
                    }
                }
                if (month2 == 3) {
                    if (day3 < 1) {
                        day3 = 28;
                        month3 = 2;
                        year3 = year2;
                    }
                    if (day3 > 31) {
                        day3 = 1;
                        month3 = 4;
                        year3 = year2;
                    }
                }
                if (month2 == 4 || month2 == 6 || month2 == 9 || month2 == 11) {
                    if (day3 < 1) {
                        day3 = 31;
                        month3 = month2 - 1;
                        year3 = year2;
                    }
                    if (day3 > 31) {
                        day3 = 1;
                        month3 = month2 + 1;
                        year3 = year2;
                    }
                }
                if (month2 == 5 || month2 == 7 || month2 == 8 || month2 == 10) {
                    if (day3 < 1) {
                        day3 = 30;
                        month3 = month2 - 1;
                        year3 = year2;
                    }
                    if (day3 > 31) {
                        day3 = 1;
                        month3 = month2 + 1;
                        year3 = year2;
                    }
                }
                if (month2 == 12) {
                    if (day3 < 1) {
                        day3 = 30;
                        month3 = 11;
                        year3 = year2;
                    }
                    if (day3 > 31) {
                        day3 = 1;
                        month3 = 1;
                        year3 = year2 + 1;
                    }
                }
                System.out.println(month3 + "-" + day3 + "-" + year3);
                String dat = String.valueOf(day3) + "-" + String.valueOf(month3) + "-" + String.valueOf(year3);
                Sample3 ss = new Sample3();
                ss.setSupplierID(suppid);
                ss.setBorrowID(String.valueOf(borrid));
                borrid += 1;
                ss.setActualRetDate(dat);
                dat = String.valueOf(day2) + "-" + String.valueOf(month2) + "-" + String.valueOf(year2);
                ss.setDateClaimToRet(dat);
                dat = String.valueOf(day) + "-" + String.valueOf(month) + "-" + String.valueOf(year);
                ss.setDateOfBorrow(dat);
                ss.setCustID(String.valueOf(custid.get(cus)));
                ss.setBookID(String.valueOf(bookid.get(boo)));
                l.add(ss);

            }
            final BorrowedDO Item = new BorrowedDO();
            for (int i = 0; i < l.size(); i++) {
                final int jj = i;
                Item.setActualRetDate(l.get(i).getActualRetDate());
                Item.setDateClaimToRet(l.get(i).getDateClaimToRet());
                Item.setDateOfBorrow(l.get(i).getDateOfBorrow());
                Item.setCustID(l.get(i).getCustID());
                Item.setBookID(l.get(i).getBookID());
                Item.setBorrowID(l.get(i).getBorrowID());
                Item.setSupplierID(l.get(i).getSupplierID());
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        dynamoDBMapper.save(Item);
                        // Item saved
                        System.out.println("hey" + jj);
                    }
                }).start();
            /*Toast toast=Toast.makeText(getApplicationContext(),"hey"+i,Toast.LENGTH_LONG);
            toast.setMargin(50,50);
            toast.show();*/
                //System.out.println("hey"+i);
            }
            System.out.println("finished");
        }
    }});
        t3.run();
        try {
            t3.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }}