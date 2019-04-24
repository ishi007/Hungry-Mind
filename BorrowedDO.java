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

@DynamoDBTable(tableName = "hungrymind-mobilehub-593518188-Borrowed")

public class BorrowedDO {
    private String _borrowID;
    private String _actualRetDate;
    private String _bookID;
    private String _custID;
    private String _dateClaimToRet;
    private String _dateOfBorrow;
    private String _supplierID;

    @DynamoDBHashKey(attributeName = "BorrowID")
    @DynamoDBAttribute(attributeName = "BorrowID")
    public String getBorrowID() {
        return _borrowID;
    }

    public void setBorrowID(final String _borrowID) {
        this._borrowID = _borrowID;
    }
    @DynamoDBAttribute(attributeName = "ActualRetDate")
    public String getActualRetDate() {
        return _actualRetDate;
    }

    public void setActualRetDate(final String _actualRetDate) {
        this._actualRetDate = _actualRetDate;
    }
    @DynamoDBAttribute(attributeName = "BookID")
    public String getBookID() {
        return _bookID;
    }

    public void setBookID(final String _bookID) {
        this._bookID = _bookID;
    }
    @DynamoDBAttribute(attributeName = "CustID")
    public String getCustID() {
        return _custID;
    }

    public void setCustID(final String _custID) {
        this._custID = _custID;
    }
    @DynamoDBAttribute(attributeName = "DateClaimToRet")
    public String getDateClaimToRet() {
        return _dateClaimToRet;
    }

    public void setDateClaimToRet(final String _dateClaimToRet) {
        this._dateClaimToRet = _dateClaimToRet;
    }
    @DynamoDBAttribute(attributeName = "DateOfBorrow")
    public String getDateOfBorrow() {
        return _dateOfBorrow;
    }

    public void setDateOfBorrow(final String _dateOfBorrow) {
        this._dateOfBorrow = _dateOfBorrow;
    }
    @DynamoDBAttribute(attributeName = "SupplierID")
    public String getSupplierID() {
        return _supplierID;
    }

    public void setSupplierID(final String _supplierID) {
        this._supplierID = _supplierID;
    }

}
