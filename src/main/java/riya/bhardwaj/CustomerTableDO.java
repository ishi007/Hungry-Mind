package riya.bhardwaj;

import com.amazonaws.mobileconnectors.dynamodbv2.dynamodbmapper.DynamoDBAttribute;
import com.amazonaws.mobileconnectors.dynamodbv2.dynamodbmapper.DynamoDBHashKey;
import com.amazonaws.mobileconnectors.dynamodbv2.dynamodbmapper.DynamoDBIndexHashKey;
import com.amazonaws.mobileconnectors.dynamodbv2.dynamodbmapper.DynamoDBIndexRangeKey;
import com.amazonaws.mobileconnectors.dynamodbv2.dynamodbmapper.DynamoDBRangeKey;
import com.amazonaws.mobileconnectors.dynamodbv2.dynamodbmapper.DynamoDBTable;

import java.util.List;
import java.util.Map;
import java.util.Set;

@DynamoDBTable(tableName = "hungrymind-mobilehub-593518188-Customer_Table")

public class CustomerTableDO {
    private String _custEmail;
    private Double _custId;
    private String _custAddress;
    private String _custName;
    private Double _custNumber;
    private String _custPassword;

    @DynamoDBHashKey(attributeName = "custEmail")
    @DynamoDBAttribute(attributeName = "custEmail")
    public String getCustEmail() {
        return _custEmail;
    }

    public void setCustEmail(final String _custEmail) {
        this._custEmail = _custEmail;
    }
    @DynamoDBRangeKey(attributeName = "custId")
    @DynamoDBAttribute(attributeName = "custId")
    public Double getCustId() {
        return _custId;
    }

    public void setCustId(final Double _custId) {
        this._custId = _custId;
    }
    @DynamoDBAttribute(attributeName = "custAddress")
    public String getCustAddress() {
        return _custAddress;
    }

    public void setCustAddress(final String _custAddress) {
        this._custAddress = _custAddress;
    }
    @DynamoDBAttribute(attributeName = "custName")
    public String getCustName() {
        return _custName;
    }

    public void setCustName(final String _custName) {
        this._custName = _custName;
    }
    @DynamoDBAttribute(attributeName = "custNumber")
    public Double getCustNumber() {
        return _custNumber;
    }

    public void setCustNumber(final Double _custNumber) {
        this._custNumber = _custNumber;
    }
    @DynamoDBAttribute(attributeName = "custPassword")
    public String getCustPassword() {
        return _custPassword;
    }

    public void setCustPassword(final String _custPassword) {
        this._custPassword = _custPassword;
    }

}
