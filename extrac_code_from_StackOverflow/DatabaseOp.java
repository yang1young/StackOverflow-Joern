import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

/**
 * Created by Qiao Yang on 29/12/2016.
 */
public class DatabaseOp {

    private String url = "jdbc:mysql://localhost/codetag";
    private String user = "root";
    private String pwd = "1qazxc";
    private Connection conn;

    DatabaseOp(String url, String user, String pwd) {
        setPwd(pwd);
        setUrl(url);
        setUser(user);
        try {
            Class.forName("com.mysql.jdbc.Driver").newInstance();
            setConn(DriverManager.getConnection(url, user, pwd));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    DatabaseOp() {
        try {
            Class.forName("com.mysql.jdbc.Driver").newInstance();
            setConn(DriverManager.getConnection(url, user, pwd));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public ResultSet search(String sql) {
        try {
            Statement st = conn.createStatement();
            ResultSet rs = st.executeQuery(sql);
            return rs;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public void insert(String sql) {

        try {
            Statement st = conn.createStatement();
            st.execute(sql);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void disConnect() {
        try {
            conn.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void setUrl(String url) {
        this.url = url;
    }


    public void setUser(String user) {
        this.user = user;
    }

    public void setPwd(String pwd) {
        this.pwd = pwd;
    }


    public void setConn(Connection conn) {
        this.conn = conn;
    }


}


/*
create table Posts         (
Id int unsigned primary key,
PostTypeId tinyint unsigned,
AcceptedAnswerId smallint unsigned,
ParentId int unsigned,
CreationDate timestamp,
Score smallint unsigned,
ViewCount int unsigned,
Body Text,
OwnerUserId int,
OwnerDisplayName varchar(40),
LastEditorUserId int unsigned,
LastEditorDisplyName varchar(60),
LastEditDate timestamp,
LastActivityDate timestamp,
Title tinytext,
Tags varchar(100),
AnswerCount smallint unsigned,
CommentCount smallint unsigned,
FavoriteCount smallint unsigned,
ClosedDate timestamp,
CommunityOwnedDate timestamp
);

/*
create table SampleC (
Id int unsigned primary key,
Score smallint unsigned,
Title tinytext,
Question Text,
Answer1 Text,
Answer2 Text,
Answer3 Text,
Answer4 Text,
Answer5 Text,
Tags varchar(100)
);



create table SampleC (
Id int unsigned primary key,
Code Text,
Tags varchar(100)
);

create table selectTag (
Id int unsigned primary key,
Code Text,
Tags varchar(100)
);

create table selectTagType (
Id int unsigned primary key,
Code Text,
Type Text,
Tags varchar(100)
);

create table SampleC (
Id int unsigned primary key,
Code Text,
Tags varchar(100)
);

create table cleanSample (
Id int unsigned primary key,
Code Text,
Tags varchar(100)
);

create table codeAST (
Id int unsigned primary key,
Code Text,
AST Text,
Tags varchar(100)
);
 */